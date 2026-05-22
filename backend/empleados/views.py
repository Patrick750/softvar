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