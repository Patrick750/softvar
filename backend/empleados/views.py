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

    def perform_destroy(self, instance):
        # Eliminar también el User asociado para que no pueda seguir iniciando sesión
        user = instance.user
        instance.delete()
        if user:
            user.delete()

    def _maybe_restrict_fields(self, request, employee_id):
        if not employee_id:
            return
        user = request.user
        try:
            employee_obj = Empleado.objects.get(id=employee_id)
        except Empleado.DoesNotExist:
            # Let the normal flow handle 404
            return
        if user.empleado and user.empleado.id == employee_obj.id:
            user_role = get_user_role(user)
            if user_role not in ['ADMIN_RRHH', 'ADMIN_SISTEMA']:
                allowed_fields = {'nombres', 'apellidos', 'telefono'}
                # We need to modify request.data
                # Since request.data might be a QueryDict, we make it mutable
                if hasattr(request.data, '_mutable'):
                    request.data._mutable = True
                for key in list(request.data.keys()):
                    if key not in allowed_fields:
                        del request.data[key]
                if hasattr(request.data, '_mutable'):
                    request.data._mutable = False

    def partial_update(self, request, *args, **kwargs):
        self._maybe_restrict_fields(request, kwargs.get('pk'))
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._maybe_restrict_fields(request, kwargs.get('pk'))
        return super().update(request, *args, **kwargs)


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

from .utils import registrar_auditoria, get_parametro, get_parametros

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

    solicitar_manual = request.data.get('solicitar_manual', False)

    # Validar duplicados solo en flujo automático
    # En solicitudes manuales el admin decide, y si el auto falló (FALLIDO)
    # el usuario debe poder recurrir al formulario manual
    if not solicitar_manual and Asistencia.objects.filter(
        empleado=empleado,
        tipo=tipo,
        estado__in=['EXITO', 'PENDIENTE_APROBACION'],
        fecha_hora__date=timezone.localdate(),
    ).exists():
        tipo_label = 'entrada' if tipo == 'ENTRADA' else 'salida'
        return Response({
            'message': f'Ya registraste tu {tipo_label} hoy. No puedes registrar otra {tipo_label} el mismo día.',
            'status': 'DUPLICADO'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    latitud_cap = request.data.get('latitud')
    longitud_cap = request.data.get('longitud')
    descriptor_cap = request.data.get('descriptor_facial') # List of 128 numbers
    liveness_score_cap = request.data.get('liveness_score') # Liveness score from frontend
    liveness_validated_cap = request.data.get('liveness_validated', False)
    justificacion = request.data.get('justificacion', '')

    # Fetch configuration limits (una sola consulta a la BD)
    try:
        params_oficina = get_parametros([
            ('OFICINA_LATITUD', '2.927300', 'Latitud centro de la sede'),
            ('OFICINA_LONGITUD', '-75.281800', 'Longitud centro de la sede'),
            ('OFICINA_RADIO_METROS', '100.0', 'Radio permitido en metros'),
        ])
        lat_oficina = float(params_oficina['OFICINA_LATITUD'])
        lon_oficina = float(params_oficina['OFICINA_LONGITUD'])
        radio_limite = float(params_oficina['OFICINA_RADIO_METROS'])
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
    no_facial_data = not empleado.foto_facial or not empleado.foto_facial_registrada
    if descriptor_cap:
        if no_facial_data:
            # No stored facial data to compare against
            face_ok = False
            face_score = None
        else:
            face_score = calcular_distancia_facial(empleado.foto_facial, descriptor_cap)
            if face_score is None or face_score > 0.6: # Euclidean distance threshold of 0.6 represents ~80% similarity
                face_ok = False
    else:
        face_ok = False # Face biometrics is mandatory for automatic validation

    if not gps_ok or not face_ok:
        # Determine type of failure
        if not face_ok and gps_ok:
            # Facial mismatch -> potential fraud
            estado = 'FRAUDE'
            observaciones = f"Intento de fraude facial detectado. Score={face_score:.3f}, umbral=0.6"
            audit_action = 'INTENTO_FRAUDE_ASISTENCIA'
            message = 'Intento de fraude detectado. Rostro no coincide con el registrado.'
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            # GPS failure or both -> regular failed attempt
            estado = 'FALLIDO'
            failure_reasons = []
            if not gps_ok:
                failure_reasons.append(f"GPS fuera de rango (Distancia={distancia:.1f}m)")
            if not face_ok:
                if no_facial_data:
                    failure_reasons.append("No hay foto facial registrada para este empleado")
                elif face_score is None:
                    failure_reasons.append("No se pudo calcular la comparación facial")
                else:
                    failure_reasons.append(f"Rostro no coincide (Score={face_score:.3f}, umbral=0.6)")
            observaciones = "Fallo de verificación. " + ". ".join(failure_reasons)
            audit_action = 'INTENTO_FALLIDO_ASISTENCIA'
            message = 'No se pudo verificar su asistencia de forma automática.'
            status_code = status.HTTP_400_BAD_REQUEST

        # Save attempt
        asistencia = Asistencia.objects.create(
            empleado=empleado,
            tipo=tipo,
            estado=estado,
            latitud=latitud_cap,
            longitud=longitud_cap,
            verificacion_facial_score=face_score,
            liveness_score=liveness_score_cap,
            liveness_validated=liveness_validated_cap,
            observaciones=observaciones
        )

        # Auditoría log
        registrar_auditoria(
            user, audit_action, 'asistencias', asistencia.id,
            None,
            {
                'tipo': tipo,
                'gps_ok': gps_ok,
                'distancia': distancia,
                'face_ok': face_ok,
                'face_score': face_score,
                'liveness_score': liveness_score_cap,
                'liveness_validated': liveness_validated_cap
            },
            request
        )

        return Response({
            'status': estado,
            'gps_ok': gps_ok,
            'face_ok': face_ok,
            'distancia': distancia,
            'face_score': face_score,
            'message': message
        }, status=status_code)

    # Validation succeeds!
    asistencia = Asistencia.objects.create(
        empleado=empleado,
        tipo=tipo,
        estado='EXITO',
        latitud=latitud_cap,
        longitud=longitud_cap,
        verificacion_facial_score=face_score,
        liveness_score=liveness_score_cap,
        liveness_validated=liveness_validated_cap,
        observaciones='Registro biométrico y GPS exitoso'
    )
    
    # Audit log
    registrar_auditoria(user, 'REGISTRO_ASISTENCIA_OK', 'asistencias', asistencia.id, None, {'tipo': tipo, 'liveness_score': liveness_score_cap, 'liveness_validated': liveness_validated_cap}, request)
    
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
@permission_classes([permissions.IsAuthenticated])
def configuracion_parametros_view(request):
    """
    Permite obtener y actualizar los parámetros de configuración del sistema.
    Requiere rol ADMIN_SISTEMA (crear/actualizar parámetros) o ADMIN_RRHH (solo lectura).
    """
    role = get_user_role(request.user)
    if role != 'ADMIN_SISTEMA':
        return Response({'error': 'Solo el Administrador del Sistema puede acceder a esta configuración'}, status=status.HTTP_403_FORBIDDEN)
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
@permission_classes([permissions.IsAuthenticated])
def auditoria_logs_view(request):
    role = get_user_role(request.user)
    if role != 'ADMIN_SISTEMA':
        return Response({'error': 'Solo el Administrador del Sistema puede ver la auditoría'}, status=status.HTTP_403_FORBIDDEN)
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
from decimal import Decimal
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.conf import settings as django_settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .nomina_engine import calcular_nomina_empleado, guardar_liquidacion
from .models import Empleado, Asistencia, Auditoria, ParametroSistema, LiquidacionNomina, Desprendible

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


# ============================================
# NÓMINA — API Views
# ============================================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def calcular_nomina_view(request):
    """
    Calcula la nómina para un período específico.
    Roles permitidos: CONTADOR, ADMIN_RRHH
    """
    role = get_user_role(request.user)
    if role not in ['CONTADOR', 'ADMIN_RRHH']:
        return Response({'error': 'No tienes permisos para calcular nómina'}, status=status.HTTP_403_FORBIDDEN)

    periodo_inicio_str = request.data.get('periodo_inicio')
    periodo_fin_str = request.data.get('periodo_fin')
    empleado_id = request.data.get('empleado_id')  # Opcional: si no se envía, calcula todos los activos

    if not periodo_inicio_str or not periodo_fin_str:
        return Response({'error': 'periodo_inicio y periodo_fin son requeridos (YYYY-MM-DD)'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        periodo_inicio = datetime.strptime(periodo_inicio_str, '%Y-%m-%d').date()
        periodo_fin = datetime.strptime(periodo_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

    if periodo_inicio > periodo_fin:
        return Response({'error': 'periodo_inicio debe ser anterior a periodo_fin'}, status=status.HTTP_400_BAD_REQUEST)

    if empleado_id:
        try:
            empleados = Empleado.objects.filter(id=empleado_id, activo=True)
            if not empleados.exists():
                return Response({'error': 'Empleado no encontrado o inactivo'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'ID de empleado inválido'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        empleados = Empleado.objects.filter(activo=True)

    if not empleados.exists():
        return Response({'error': 'No hay empleados activos para liquidar'}, status=status.HTTP_400_BAD_REQUEST)

    resultados = []
    for emp in empleados:
        try:
            calculo = calcular_nomina_empleado(emp, periodo_inicio, periodo_fin, request.user, request)
            liquidacion = guardar_liquidacion(emp, calculo, periodo_inicio, periodo_fin, request.user, request)

            resultados.append({
                'liquidacion_id': liquidacion.id,
                'empleado_id': emp.id,
                'nombres': emp.nombres,
                'apellidos': emp.apellidos,
                'cedula': emp.cedula,
                'cargo': emp.cargo,
                'salario_base': str(calculo['salario_base']),
                'valor_hora': str(calculo['valor_hora']),
                'horas_trabajadas': str(calculo['horas_trabajadas']),
                'horas_extra_diurnas': str(calculo['horas_extra_diurnas']),
                'horas_extra_nocturnas': str(calculo['horas_extra_nocturnas']),
                'horas_dominicales': str(calculo['horas_dominicales']),
                'recargo_diurno': str(calculo['recargo_diurno']),
                'recargo_nocturno': str(calculo['recargo_nocturno']),
                'recargo_dominical': str(calculo['recargo_dominical']),
                'devengado_total': str(calculo['total_devengado']),
                'descuento_salud': str(calculo['descuento_salud']),
                'descuento_pension': str(calculo['descuento_pension']),
                'descuento_arl': str(calculo['descuento_arl']),
                'deducciones_total': str(calculo['total_deducciones']),
                'neto_pagar': str(calculo['neto_pagar']),
                'dias_liquidados': calculo['dias_liquidados'],
                'estado': liquidacion.estado,
            })
        except Exception as e:
            resultados.append({
                'empleado_id': emp.id,
                'nombres': emp.nombres,
                'apellidos': emp.apellidos,
                'error': str(e),
            })

    # Resumen
    total_devengados = sum(Decimal(r.get('devengado_total', '0')) for r in resultados if 'devengado_total' in r)
    total_deducciones = sum(Decimal(r.get('deducciones_total', '0')) for r in resultados if 'deducciones_total' in r)
    total_neto = sum(Decimal(r.get('neto_pagar', '0')) for r in resultados if 'neto_pagar' in r)

    return Response({
        'periodo_inicio': periodo_inicio_str,
        'periodo_fin': periodo_fin_str,
        'total_empleados': len(resultados),
        'total_devengados': str(total_devengados),
        'total_deducciones': str(total_deducciones),
        'total_neto': str(total_neto),
        'resultados': resultados,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def listar_liquidaciones_view(request):
    """Lista las liquidaciones de nómina, opcionalmente filtradas por período y empleado."""
    role = get_user_role(request.user)
    if role not in ['CONTADOR', 'ADMIN_RRHH']:
        return Response({'error': 'No tienes permisos para ver liquidaciones'}, status=status.HTTP_403_FORBIDDEN)

    qs = LiquidacionNomina.objects.select_related('empleado').all()

    periodo = request.query_params.get('periodo')  # YYYY-MM
    empleado_id = request.query_params.get('empleado_id')

    if periodo:
        try:
            anio, mes = periodo.split('-')
            qs = qs.filter(periodo_inicio__year=int(anio), periodo_inicio__month=int(mes))
        except (ValueError, IndexError):
            pass

    if empleado_id:
        qs = qs.filter(empleado_id=empleado_id)

    data = []
    for liq in qs:
        data.append({
            'id': liq.id,
            'empleado_id': liq.empleado_id,
            'empleado_nombre': f"{liq.empleado.nombres} {liq.empleado.apellidos}",
            'empleado_cedula': liq.empleado.cedula,
            'periodo_inicio': liq.periodo_inicio.isoformat(),
            'periodo_fin': liq.periodo_fin.isoformat(),
            'salario_base': str(liq.salario_base),
            'total_devengado': str(liq.total_devengado),
            'total_deducciones': str(liq.total_deducciones),
            'neto_pagar': str(liq.neto_pagar),
            'dias_liquidados': liq.dias_liquidados,
            'estado': liq.estado,
            'created_at': liq.created_at.isoformat(),
        })

    return Response(data)


# ============================================
# DESPRENDIBLES PDF — API Views
# ============================================

def generar_pdf_desprendible(liquidacion):
    """
    Genera un PDF de desprendible de nómina usando ReportLab.
    Retorna el PDF como bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=18, textColor=colors.HexColor('#042C53'),
        spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#5F5E5A'),
        alignment=TA_CENTER, spaceAfter=12
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'],
        fontSize=11, textColor=colors.HexColor('#185FA5'),
        spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold'
    )
    label_style = ParagraphStyle(
        'Label', parent=styles['Normal'],
        fontSize=8, textColor=colors.HexColor('#5F5E5A'),
        fontName='Helvetica'
    )
    value_style = ParagraphStyle(
        'Value', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#2C2C2A'),
        fontName='Helvetica-Bold', spaceAfter=6
    )
    total_style = ParagraphStyle(
        'Total', parent=styles['Normal'],
        fontSize=12, textColor=colors.HexColor('#3B6D11'),
        fontName='Helvetica-Bold', alignment=TA_RIGHT
    )

    empleado = liquidacion.empleado
    elements = []

    # Encabezado
    elements.append(Paragraph("SOFTVAR S.A.S.", title_style))
    elements.append(Paragraph("Sistema de Control de Asistencia y Nómina", subtitle_style))
    elements.append(Paragraph("Desprendible de Pago", subtitle_style))
    elements.append(Spacer(1, 10))

    # Línea divisora
    elements.append(Table([['']], colWidths=[460], style=TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#185FA5')),
    ])))
    elements.append(Spacer(1, 8))

    # Información del empleado
    elements.append(Paragraph("DATOS DEL EMPLEADO", section_style))
    emp_data = [
        [Paragraph("Nombre:", label_style), Paragraph(f"{empleado.nombres} {empleado.apellidos}", value_style),
         Paragraph("Cédula:", label_style), Paragraph(str(empleado.cedula), value_style)],
        [Paragraph("Cargo:", label_style), Paragraph(str(empleado.cargo), value_style),
         Paragraph("Período:", label_style), Paragraph(f"{liquidacion.periodo_inicio} al {liquidacion.periodo_fin}", value_style)],
        [Paragraph("Días liquidados:", label_style), Paragraph(str(liquidacion.dias_liquidados), value_style),
         Paragraph("Salario Base:", label_style), Paragraph(f"${float(liquidacion.salario_base):,.2f}", value_style)],
    ]
    emp_table = Table(emp_data, colWidths=[65, 165, 65, 165])
    emp_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(emp_table)
    elements.append(Spacer(1, 10))

    # Tabla de Devengados
    elements.append(Paragraph("DEVENGADOS", section_style))
    dev_data = [
        [Paragraph("Concepto", label_style), Paragraph("Horas", label_style), Paragraph("Valor", label_style)],
        [Paragraph("Salario Base"), Paragraph("-"), Paragraph(f"${float(liquidacion.salario_base):,.2f}")],
    ]
    if liquidacion.horas_extra_diurnas > 0:
        dev_data.append([
            Paragraph("Horas Extra Diurnas (25%)"),
            Paragraph(str(liquidacion.horas_extra_diurnas)),
            Paragraph(f"${float(liquidacion.recargo_diurno):,.2f}"),
        ])
    if liquidacion.horas_extra_nocturnas > 0:
        dev_data.append([
            Paragraph("Horas Extra Nocturnas (75%)"),
            Paragraph(str(liquidacion.horas_extra_nocturnas)),
            Paragraph(f"${float(liquidacion.recargo_nocturno):,.2f}"),
        ])
    if liquidacion.horas_dominicales > 0:
        dev_data.append([
            Paragraph("Recargo Dominical/Festivo"),
            Paragraph(str(liquidacion.horas_dominicales)),
            Paragraph(f"${float(liquidacion.recargo_dominical):,.2f}"),
        ])
    dev_data.append([
        Paragraph("<b>TOTAL DEVENGADO</b>"),
        Paragraph(""),
        Paragraph(f"<b>${float(liquidacion.total_devengado):,.2f}</b>"),
    ])

    dev_table = Table(dev_data, colWidths=[230, 100, 130])
    dev_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D1C7')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F1FB')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#EAF3DE')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elements.append(dev_table)
    elements.append(Spacer(1, 10))

    # Tabla de Deducciones
    elements.append(Paragraph("DEDUCCIONES", section_style))
    ded_data = [
        [Paragraph("Concepto", label_style), Paragraph("Porcentaje", label_style), Paragraph("Valor", label_style)],
        [Paragraph("Salud"), Paragraph("4%"), Paragraph(f"${float(liquidacion.descuento_salud):,.2f}")],
        [Paragraph("Pensión"), Paragraph("4%"), Paragraph(f"${float(liquidacion.descuento_pension):,.2f}")],
        [Paragraph("ARL"), Paragraph("Variable"), Paragraph(f"${float(liquidacion.descuento_arl):,.2f}")],
        [
            Paragraph("<b>TOTAL DEDUCCIONES</b>"),
            Paragraph(""),
            Paragraph(f"<b>${float(liquidacion.total_deducciones):,.2f}</b>"),
        ],
    ]
    ded_table = Table(ded_data, colWidths=[230, 100, 130])
    ded_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D1C7')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FCEBEB')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FCEBEB')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elements.append(ded_table)
    elements.append(Spacer(1, 12))

    # Neto a pagar
    elements.append(Paragraph(
        f"NETO A PAGAR: ${float(liquidacion.neto_pagar):,.2f}", total_style
    ))

    # Línea final
    elements.append(Spacer(1, 15))
    elements.append(Table([['']], colWidths=[460], style=TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#185FA5')),
    ])))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "Este es un documento informativo generado por SoftVar S.A.S.",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7, textColor=colors.HexColor('#B4B2A9'), alignment=TA_CENTER)
    ))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generar_desprendible_view(request):
    """
    Genera un PDF de desprendible para una liquidación específica.
    Roles permitidos: CONTADOR, ADMIN_RRHH
    """
    role = get_user_role(request.user)
    if role not in ['CONTADOR', 'ADMIN_RRHH']:
        return Response({'error': 'No tienes permisos para generar desprendibles'}, status=status.HTTP_403_FORBIDDEN)

    liquidacion_id = request.data.get('liquidacion_id')
    if not liquidacion_id:
        return Response({'error': 'liquidacion_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        liquidacion = LiquidacionNomina.objects.select_related('empleado').get(id=liquidacion_id)
    except LiquidacionNomina.DoesNotExist:
        return Response({'error': 'Liquidación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    try:
        pdf_bytes = generar_pdf_desprendible(liquidacion)
        import base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        periodo_str = liquidacion.periodo_fin.strftime('%Y-%m')

        # Guardar o actualizar el desprendible
        desprendible, created = Desprendible.objects.update_or_create(
            liquidacion=liquidacion,
            empleado=liquidacion.empleado,
            periodo=periodo_str,
            defaults={
                'archivo_pdf': pdf_base64,
                'estado': 'GENERADO',
            }
        )

        registrar_auditoria(
            request.user, 'GENERAR_DESPRENDIBLE', 'desprendibles', desprendible.id,
            None,
            {'empleado_id': liquidacion.empleado.id, 'periodo': periodo_str},
            request
        )

        return Response({
            'desprendible_id': desprendible.id,
            'empleado_nombre': f"{liquidacion.empleado.nombres} {liquidacion.empleado.apellidos}",
            'periodo': periodo_str,
            'neto_pagar': str(liquidacion.neto_pagar),
            'estado': 'GENERADO',
            'pdf_base64': pdf_base64,
            'message': 'Desprendible generado con éxito.',
        })

    except Exception as e:
        return Response({'error': f'Error generando PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enviar_desprendible_view(request):
    """
    Envía el desprendible de nómina por correo electrónico al empleado.
    """
    role = get_user_role(request.user)
    if role not in ['CONTADOR', 'ADMIN_RRHH']:
        return Response({'error': 'No tienes permisos para enviar desprendibles'}, status=status.HTTP_403_FORBIDDEN)

    desprendible_id = request.data.get('desprendible_id')
    if not desprendible_id:
        return Response({'error': 'desprendible_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        desprendible = Desprendible.objects.select_related('empleado', 'liquidacion').get(id=desprendible_id)
    except Desprendible.DoesNotExist:
        return Response({'error': 'Desprendible no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    empleado = desprendible.empleado
    if not empleado.email:
        return Response({'error': 'El empleado no tiene correo electrónico registrado'}, status=status.HTTP_400_BAD_REQUEST)

    # Si no tiene PDF, generarlo primero
    if not desprendible.archivo_pdf:
        try:
            pdf_bytes = generar_pdf_desprendible(desprendible.liquidacion)
            import base64
            desprendible.archivo_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            desprendible.save()
        except Exception as e:
            return Response({'error': f'Error generando PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        import base64
        pdf_bytes = base64.b64decode(desprendible.archivo_pdf)

    try:
        # Crear y enviar el email
        import base64
        email = EmailMessage(
            subject=f'Desprendible de Nómina - {desprendible.periodo} - SoftVar',
            body=f"""Hola {empleado.nombres} {empleado.apellidos},

Adjunto encontrarás tu desprendible de nómina correspondiente al período {desprendible.periodo}.

El neto a pagar es de ${float(desprendible.liquidacion.neto_pagar):,.2f} COP.

Puedes revisar el detalle completo en el archivo adjunto.

Atentamente,
El Equipo de Recursos Humanos
SoftVar S.A.S.""",
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            to=[empleado.email],
        )
        email.attach(f'desprendible_nomina_{desprendible.periodo}.pdf', pdf_bytes, 'application/pdf')
        email.send(fail_silently=False)

        # Actualizar estado
        desprendible.estado = 'ENVIADO'
        desprendible.fecha_envio = timezone.now()
        desprendible.email_enviado_a = empleado.email
        desprendible.save()

        registrar_auditoria(
            request.user, 'ENVIAR_DESPRENDIBLE', 'desprendibles', desprendible.id,
            {'estado': 'GENERADO'},
            {'estado': 'ENVIADO', 'email': empleado.email, 'periodo': desprendible.periodo},
            request
        )

        return Response({
            'message': 'Desprendible enviado con éxito.',
            'email_enviado_a': empleado.email,
            'estado': 'ENVIADO',
        })

    except Exception as e:
        desprendible.estado = 'FALLIDO'
        desprendible.error_mensaje = str(e)
        desprendible.save()

        registrar_auditoria(
            request.user, 'ERROR_ENVIAR_DESPRENDIBLE', 'desprendibles', desprendible.id,
            None,
            {'error': str(e), 'email': empleado.email, 'periodo': desprendible.periodo},
            request
        )

        return Response({'error': f'Error enviando email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)