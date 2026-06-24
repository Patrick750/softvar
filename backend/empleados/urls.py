from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpleadoViewSet, login_view, csrf_token_view,
    registrar_asistencia_view, historial_asistencia_view,
    asistencias_pendientes_view, aprobar_asistencia_view,
    configuracion_parametros_view, auditoria_logs_view,
    get_mi_perfil_view, cambiar_contrasena_view,
    recuperar_contrasena_view, NominaViewSet,
    dashboard_reportes_view, generar_reporte_view
)

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'nomina', NominaViewSet, basename='nomina')

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/csrf/', csrf_token_view, name='auth-csrf'),
    path('auth/password/', cambiar_contrasena_view, name='auth-password'),
    path('auth/recuperar-contrasena/', recuperar_contrasena_view, name='auth-recuperar-contrasena'),
    
    path('asistencia/registrar/', registrar_asistencia_view, name='asistencia-registrar'),
    path('asistencia/historial/', historial_asistencia_view, name='asistencia-historial'),
    path('asistencia/pendientes/', asistencias_pendientes_view, name='asistencia-pendientes'),
    path('asistencia/aprobar/', aprobar_asistencia_view, name='asistencia-aprobar'),
    path('configuracion/parametros/', configuracion_parametros_view, name='configuracion-parametros'),
    path('auditoria/logs/', auditoria_logs_view, name='auditoria-logs'),
    
    path('reportes/dashboard/', dashboard_reportes_view, name='reportes-dashboard'),
    path('reportes/generar/', generar_reporte_view, name='reportes-generar'),
    
    path('empleados/me/', get_mi_perfil_view, name='empleado-me'),
    path('', include(router.urls)),
]