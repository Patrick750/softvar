"""
Utilidades compartidas — Sistema SoftVar
Funciones helper usadas por múltiples módulos para evitar importaciones circulares.
"""

import json
from .models import Auditoria, ParametroSistema


def registrar_auditoria(user, accion, tabla_afectada, registro_id=None, valor_anterior=None, valor_nuevo=None, request=None):
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

    def clean_val(v):
        if v is None:
            return None
        if isinstance(v, (dict, list)):
            return json.dumps(v)
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
