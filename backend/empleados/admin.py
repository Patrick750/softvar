from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'cargo', 'activo')
    search_fields = ('cedula', 'nombres', 'apellidos')
    list_filter = ('activo', 'tipo_contrato')
    readonly_fields = ('created_at', 'updated_at')