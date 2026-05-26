from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpleadoViewSet, login_view, csrf_token_view,
    registrar_asistencia_view, historial_asistencia_view,
    asistencias_pendientes_view, aprobar_asistencia_view,
    configuracion_parametros_view, auditoria_logs_view,
    get_mi_perfil_view, cambiar_contrasena_view,
    calcular_nomina_view, listar_liquidaciones_view,
    generar_desprendible_view, enviar_desprendible_view
)

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/csrf/', csrf_token_view, name='auth-csrf'),
    path('auth/password/', cambiar_contrasena_view, name='auth-password'),
    
    path('asistencia/registrar/', registrar_asistencia_view, name='asistencia-registrar'),
    path('asistencia/historial/', historial_asistencia_view, name='asistencia-historial'),
    path('asistencia/pendientes/', asistencias_pendientes_view, name='asistencia-pendientes'),
    path('asistencia/aprobar/', aprobar_asistencia_view, name='asistencia-aprobar'),
    path('configuracion/parametros/', configuracion_parametros_view, name='configuracion-parametros'),
    path('auditoria/logs/', auditoria_logs_view, name='auditoria-logs'),
    
    path('empleados/me/', get_mi_perfil_view, name='empleado-me'),

    # Nómina
    path('nomina/calcular/', calcular_nomina_view, name='nomina-calcular'),
    path('nomina/liquidaciones/', listar_liquidaciones_view, name='nomina-liquidaciones'),

    # Desprendibles PDF
    path('desprendibles/generar/', generar_desprendible_view, name='desprendibles-generar'),
    path('desprendibles/enviar/', enviar_desprendible_view, name='desprendibles-enviar'),

    path('', include(router.urls)),
]