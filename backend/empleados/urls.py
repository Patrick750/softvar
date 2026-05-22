from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, login_view, csrf_token_view

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/csrf/', csrf_token_view, name='auth-csrf'),
    path('', include(router.urls)),
]