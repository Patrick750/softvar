from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from .models import Empleado
from .serializers import EmpleadoSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def login_view(request):
    """
    Endpoint de inicio de sesión.
    Autentica al usuario usando email y contraseña,
    crea una sesión y devuelve los datos del usuario.
    """
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not email or not password:
        return Response(
            {'error': 'Correo electrónico y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Buscar usuario por email
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Correo electrónico o contraseña incorrectos'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Autenticar con username (Django requiere username)
    user = authenticate(request, username=user_obj.username, password=password)

    if user is None:
        return Response(
            {'error': 'Correo electrónico o contraseña incorrectos'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Cuenta desactivada. Contacte al administrador.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Crear sesión
    login(request, user)

    # Determinar el rol del usuario (primer grupo asignado o por username)
    groups = list(user.groups.values_list('name', flat=True))
    if groups:
        rol = groups[0]
    else:
        # Mapeo por defecto según username
        role_map = {
            'admin_rrhh': 'ADMIN_RRHH',
            'contador': 'CONTADOR',
            'gerente': 'GERENTE',
            'admin_sistema': 'ADMIN_SISTEMA',
        }
        rol = role_map.get(user.username, 'EMPLEADO')

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'nombre': f"{user.first_name} {user.last_name}".strip() or user.username,
        'rol': rol,
        'is_staff': user.is_staff,
    }, status=status.HTTP_200_OK)


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def csrf_token_view(request):
    """
    Endpoint para obtener el token CSRF.
    Establece la cookie csrftoken y devuelve el token en el cuerpo JSON.
    """
    return Response({
        'csrfToken': get_token(request),
    })


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['cedula', 'nombres', 'apellidos', 'email', 'cargo']
    ordering_fields = ['nombres', 'apellidos', 'salario_base', 'fecha_ingreso', 'created_at']
    ordering = ['nombres', 'apellidos']


import math
import json
from django.utils import timezone
from .models import Empleado, Asistencia, Auditoria, ParametroSistema

# Helper functions for GPS and Face recognition
def calcular_distancia_gps(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2 - lat1))
    delta_lambda = math.radians(float(lon2 - lon1))
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def calcular_distancia_facial(stored_photo_str, captured_descriptor):
    try:
        if not stored_photo_str or not captured_descriptor:
            return None
            
        stored_data = json.loads(stored_photo_str)
        stored_descriptor = stored_data.get('descriptor')
        
        if not stored_descriptor:
            return None
            
        # Euclidean distance between two 128-float arrays
        d1 = [float(x) for x in stored_descriptor]
        d2 = [float(x) for x in captured_descriptor]
        
        if len(d1) != len(d2) or len(d1) == 0:
            return None
            
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(d1, d2)))
    except Exception as e:
        print(f"Error comparing face vectors: {e}")
        return None

def registrar_auditoria(user, accion, tabla_afectada, registro_id=None, valor_anterior=None, valor_nuevo=None, request=None):
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
            
    # Normalize inputs
    def clean_val(v):
        if v is None: return None
        if isinstance(v, (dict, list)): return json.dumps(v)
        return str(v)

    Auditoria.objects.create(
        usuario=user if user and user.is_authenticated else None,
        tabla_afectada=tabla_afectada,
        registro_id=registro_id,
        accion=accion,
        valor_anterior=clean_val(valor_anterior),
        valor_nuevo=clean_val(valor_nuevo),
        ip_address=ip_address
    )

def get_parametro(clave, default_val, desc=""):
    param, created = ParametroSistema.objects.get_or_create(
        clave=clave,
        defaults={'valor': str(default_val), 'descripcion': desc}
    )
    return param.valor

# Custom permission helpers based on username/groups
def get_user_role(user):
    if not user or not user.is_authenticated:
        return 'ANONYMOUS'
    groups = list(user.groups.values_list('name', flat=True))
    if groups:
        return groups[0]
    
    role_map = {
        'admin_rrhh': 'ADMIN_RRHH',
        'contador': 'CONTADOR',
        'gerente': 'GERENTE',
        'admin_sistema': 'ADMIN_SISTEMA',
    }
    return role_map.get(user.username, 'EMPLEADO')

class IsAdminRRHH(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'ADMIN_RRHH'

class IsAdminSistema(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'ADMIN_SISTEMA'

# API Views for attendance

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def registrar_asistencia_view(request):
    user = request.user
    try:
        empleado = user.empleado
    except Empleado.DoesNotExist:
        return Response({'error': 'El usuario actual no está asociado a un Empleado'}, status=status.HTTP_400_BAD_REQUEST)
        
    tipo = request.data.get('tipo')
    if tipo not in ['ENTRADA', 'SALIDA']:
        return Response({'error': 'Tipo de registro inválido (Debe ser ENTRADA o SALIDA)'}, status=status.HTTP_400_BAD_REQUEST)
        
    latitud_cap = request.data.get('latitud')
    longitud_cap = request.data.get('longitud')
    descriptor_cap = request.data.get('descriptor_facial') # List of 128 numbers
    solicitar_manual = request.data.get('solicitar_manual', False)
    justificacion = request.data.get('justificacion', '')

    # Fetch configuration limits
    try:
        lat_oficina = float(get_parametro('OFICINA_LATITUD', '2.927300', 'Latitud centro de la sede'))
        lon_oficina = float(get_parametro('OFICINA_LONGITUD', '-75.281800', 'Longitud centro de la sede'))
        radio_limite = float(get_parametro('OFICINA_RADIO_METROS', '100.0', 'Radio permitido en metros'))
    except ValueError:
        lat_oficina, lon_oficina, radio_limite = 2.927300, -75.281800, 100.0

    # 1. Manual approval request route
    if solicitar_manual:
        if not justificacion:
            return Response({'error': 'La justificación es obligatoria para solicitud manual'}, status=status.HTTP_400_BAD_REQUEST)
        
        asistencia = Asistencia.objects.create(
            empleado=empleado,
            tipo=tipo,
            estado='PENDIENTE_APROBACION',
            latitud=latitud_cap,
            longitud=longitud_cap,
            justificacion_manual=justificacion,
            observaciones='Solicitud de marca manual por fallo de sensores'
        )
        registrar_auditoria(user, 'SOLICITAR_APROBACION_MANUAL', 'asistencias', asistencia.id, None, {'tipo': tipo, 'justificacion': justificacion}, request)
        return Response({
            'status': 'PENDIENTE',
            'message': 'Solicitud manual registrada, en espera de aprobación de RRHH.'
        }, status=status.HTTP_201_CREATED)

    # 2. Automatic validation flow
    gps_ok = True
    distancia = 0.0
    if latitud_cap is not None and longitud_cap is not None:
        distancia = calcular_distancia_gps(latitud_cap, longitud_cap, lat_oficina, lon_oficina)
        if distancia > radio_limite:
            gps_ok = False
    else:
        gps_ok = False # GPS is mandatory for automatic validation
        
    face_ok = True
    face_score = None
    if descriptor_cap:
        face_score = calcular_distancia_facial(empleado.foto_facial, descriptor_cap)
        if face_score is None or face_score > 0.6: # Euclidean distance threshold of 0.6 represents ~80% similarity
            face_ok = False
    else:
        face_ok = False # Face biometrics is mandatory for automatic validation

    if not gps_ok or not face_ok:
        # Save as failed attempt
        asistencia = Asistencia.objects.create(
            empleado=empleado,
            tipo=tipo,
            estado='FALLIDO',
            latitud=latitud_cap,
            longitud=longitud_cap,
            verificacion_facial_score=face_score,
            observaciones=f"Fallo de verificación. GPS_OK={gps_ok} (Distancia={distancia:.1f}m), FACE_OK={face_ok} (Score={face_score})"
        )
        
        # Auditoría log
        registrar_auditoria(
            user, 'INTENTO_FALLIDO_ASISTENCIA', 'asistencias', asistencia.id,
            None,
            {
                'tipo': tipo,
                'gps_ok': gps_ok,
                'distancia': distancia,
                'face_ok': face_ok,
                'face_score': face_score
            },
            request
        )
        
        return Response({
            'status': 'FALLIDO',
            'gps_ok': gps_ok,
            'face_ok': face_ok,
            'distancia': distancia,
            'face_score': face_score,
            'message': 'No se pudo verificar su asistencia de forma automática.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Validation succeeds!
    asistencia = Asistencia.objects.create(
        empleado=empleado,
        tipo=tipo,
        estado='EXITO',
        latitud=latitud_cap,
        longitud=longitud_cap,
        verificacion_facial_score=face_score,
        observaciones='Registro biométrico y GPS exitoso'
    )
    
    # Audit log
    registrar_auditoria(user, 'REGISTRO_ASISTENCIA_OK', 'asistencias', asistencia.id, None, {'tipo': tipo}, request)
    
    return Response({
        'status': 'EXITO',
        'message': 'Asistencia registrada con éxito.',
        'fecha_hora': asistencia.fecha_hora.isoformat()
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def historial_asistencia_view(request):
    user = request.user
    role = get_user_role(user)
    
    if role == 'ADMIN_RRHH':
        # Admin can view all or filter by employee
        empleado_id = request.query_params.get('empleado_id')
        if empleado_id:
            qs = Asistencia.objects.filter(empleado_id=empleado_id)
        else:
            qs = Asistencia.objects.all()
    else:
        # Standard employees can only view their own
        try:
            empleado = user.empleado
            qs = Asistencia.objects.filter(empleado=empleado)
        except Empleado.DoesNotExist:
            return Response([])

    data = []
    for ast in qs:
        data.append({
            'id': ast.id,
            'empleado_id': ast.empleado_id,
            'empleado_nombre': f"{ast.empleado.nombres} {ast.empleado.apellidos}",
            'fecha_hora': ast.fecha_hora.isoformat() if ast.fecha_hora else None,
            'tipo': ast.tipo,
            'estado': ast.estado,
            'latitud': ast.latitud,
            'longitud': ast.longitud,
            'justificacion_manual': ast.justificacion_manual,
            'aprobado_por': ast.aprobado_por.username if ast.aprobado_por else None,
            'observaciones': ast.observaciones
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminRRHH])
def asistencias_pendientes_view(request):
    qs = Asistencia.objects.filter(estado='PENDIENTE_APROBACION')
    data = []
    for ast in qs:
        data.append({
            'id': ast.id,
            'empleado_id': ast.empleado_id,
            'empleado_nombre': f"{ast.empleado.nombres} {ast.empleado.apellidos}",
            'fecha_hora': ast.fecha_hora.isoformat() if ast.fecha_hora else None,
            'tipo': ast.tipo,
            'justificacion_manual': ast.justificacion_manual
        })
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminRRHH])
def aprobar_asistencia_view(request):
    asistencia_id = request.data.get('asistencia_id')
    aprobar = request.data.get('aprobar', False) # True=Aprobar, False=Rechazar
    justificacion_admin = request.data.get('justificacion_admin', '')

    if not asistencia_id:
        return Response({'error': 'ID de asistencia es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ast = Asistencia.objects.get(id=asistencia_id, estado='PENDIENTE_APROBACION')
    except Asistencia.DoesNotExist:
        return Response({'error': 'Registro pendiente de asistencia no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    valor_anterior = {'estado': ast.estado}
    if aprobar:
        ast.estado = 'EXITO'
        ast.observaciones = f"Aprobado manualmente por {request.user.username}. {justificacion_admin}"
    else:
        ast.estado = 'RECHAZADO'
        ast.observaciones = f"Rechazado por {request.user.username}. {justificacion_admin}"

    ast.aprobado_por = request.user
    ast.save()

    valor_nuevo = {'estado': ast.estado, 'aprobado_por': request.user.username, 'observaciones': ast.observaciones}
    registrar_auditoria(request.user, 'APROBAR_ASISTENCIA_MANUAL' if aprobar else 'RECHAZAR_ASISTENCIA_MANUAL', 'asistencias', ast.id, valor_anterior, valor_nuevo, request)

    return Response({
        'message': f"Registro de asistencia {'aprobado' if aprobar else 'rechazado'} con éxito."
    })


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminSistema])
def configuracion_parametros_view(request):
    """
    Permite obtener y actualizar los parámetros de configuración del sistema.
    """
    if request.method == 'GET':
        params = ParametroSistema.objects.all()
        data = {p.clave: {'valor': p.valor, 'descripcion': p.descripcion} for p in params}
        
        # Ensure default parameters are populated
        defaults = {
            'OFICINA_LATITUD': '2.927300',
            'OFICINA_LONGITUD': '-75.281800',
            'OFICINA_RADIO_METROS': '100.0',
            'SMMLV': '1300606.00',
            'SALUD_APORTE': '4.0',
            'PENSION_APORTE': '4.0',
            'ARL_APORTE': '0.522'
        }
        for k, v in defaults.items():
            if k not in data:
                val = get_parametro(k, v, f"Parámetro {k}")
                data[k] = {'valor': val, 'descripcion': f"Parámetro {k}"}
                
        return Response(data)

    elif request.method == 'POST':
        # Update multiple parameters at once
        actualizados = []
        for clave, valor in request.data.items():
            try:
                param = ParametroSistema.objects.get(clave=clave)
                anterior = param.valor
                param.valor = str(valor)
                param.save()
                actualizados.append(clave)
                registrar_auditoria(request.user, 'ACTUALIZAR_PARAMETRO', 'parametros_sistema', param.id, {'valor': anterior}, {'valor': param.valor}, request)
            except ParametroSistema.DoesNotExist:
                param = ParametroSistema.objects.create(clave=clave, valor=str(valor))
                actualizados.append(clave)
                registrar_auditoria(request.user, 'CREAR_PARAMETRO', 'parametros_sistema', param.id, None, {'valor': param.valor}, request)
                
        return Response({'message': f"Parámetros actualizados con éxito: {', '.join(actualizados)}"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminSistema])
def auditoria_logs_view(request):
    qs = Auditoria.objects.all()[:100] # Limit to 100 logs
    data = []
    for log in qs:
        data.append({
            'id': log.id,
            'usuario': log.usuario.username if log.usuario else 'Anónimo/Sistema',
            'fecha_hora': log.fecha_hora.isoformat() if log.fecha_hora else None,
            'tabla_afectada': log.tabla_afectada,
            'registro_id': log.registro_id,
            'accion': log.accion,
            'valor_anterior': log.valor_anterior,
            'valor_nuevo': log.valor_nuevo,
            'ip_address': log.ip_address
        })
    return Response(data)


from django.contrib.auth import update_session_auth_hash

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_mi_perfil_view(request):
    try:
        empleado = request.user.empleado
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)
    except Empleado.DoesNotExist:
        return Response({'error': 'El usuario actual no tiene un perfil de Empleado asociado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cambiar_contrasena_view(request):
    user = request.user
    old_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'error': 'La contraseña actual y la nueva son requeridas'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'La contraseña actual es incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user) # Mantiene al usuario logueado en la sesión actual
    
    # Audit log
    registrar_auditoria(user, 'CAMBIO_CONTRASENA', 'auth_user', user.id, None, None, request)
    
    return Response({'message': 'Contraseña cambiada con éxito.'})