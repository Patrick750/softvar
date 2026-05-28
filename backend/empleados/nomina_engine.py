"""
Motor de cálculo de nómina — Sistema SoftVar
Conforme al CST colombiano (Código Sustantivo del Trabajo)

Cálculos:
- Valor hora base = salario_base / 240 (30 días x 8 horas)
- Hora extra diurna (HED): 25% sobre valor hora (Art. 168 CST)
- Hora extra nocturna (HEN): 75% sobre valor hora (Art. 168 CST)
- Recargo dominical/festivo: 75% sobre valor hora (Art. 179 CST)
- Salud: 4% del total devengado (Ley 100/93)
- Pensión: 4% del total devengado (Ley 100/93)
- ARL: porcentaje parametrizado sobre salario base
"""

import math
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .models import Empleado, Asistencia, ParametroSistema, LiquidacionNomina
from .utils import get_parametro, registrar_auditoria

# Constantes CST
HORAS_MES = Decimal('240')  # 30 días × 8 horas
RECARGO_HORA_EXTRA_DIURNA = Decimal('1.25')   # 25% adicional
RECARGO_HORA_EXTRA_NOCTURNA = Decimal('1.75') # 75% adicional
RECARGO_DOMINICAL_FESTIVO = Decimal('1.75')   # 75% adicional
DEDUCCION_SALUD = Decimal('0.04')              # 4%
DEDUCCION_PENSION = Decimal('0.04')            # 4%


def calcular_valor_hora(salario_base):
    """Calcula el valor de una hora de trabajo ordinario."""
    return (Decimal(str(salario_base)) / HORAS_MES).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def es_domingo_o_festivo(fecha):
    """Verifica si una fecha es domingo (simplificado)."""
    # Por simplicidad, solo verificamos domingo.
    # En producción se integraría con una API de festivos Colombia.
    return fecha.weekday() == 6  # Sunday


def calcular_horas_extras(empleado, periodo_inicio, periodo_fin):
    """
    Calcula las horas extras trabajadas por un empleado en un período.
    Analiza los registros de asistencia para determinar horas extra.
    """
    # Obtener asistencias del período
    asistencias = Asistencia.objects.filter(
        empleado=empleado,
        fecha_hora__date__gte=periodo_inicio,
        fecha_hora__date__lte=periodo_fin,
        estado='EXITO'
    ).order_by('fecha_hora')

    horas_extra_diurnas = Decimal('0')
    horas_extra_nocturnas = Decimal('0')
    horas_dominicales = Decimal('0')
    total_horas_trabajadas = Decimal('0')
    dias_liquidados = set()

    # Agrupar registros por día para calcular horas trabajadas
    registros_por_dia = {}
    for asistencia in asistencias:
        dia = asistencia.fecha_hora.date()
        if dia not in registros_por_dia:
            registros_por_dia[dia] = {'entrada': None, 'salida': None}
        if asistencia.tipo == 'ENTRADA' and registros_por_dia[dia]['entrada'] is None:
            registros_por_dia[dia]['entrada'] = asistencia.fecha_hora
        elif asistencia.tipo == 'SALIDA':
            registros_por_dia[dia]['salida'] = asistencia.fecha_hora

    for dia, registros in registros_por_dia.items():
        if registros['entrada'] and registros['salida']:
            # Calcular horas trabajadas en el día
            delta = registros['salida'] - registros['entrada']
            horas_dia = Decimal(str(delta.total_seconds() / 3600)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # Jornada ordinaria: 8 horas
            jornada_ordinaria = Decimal('8')
            if horas_dia > jornada_ordinaria:
                horas_extra = horas_dia - jornada_ordinaria
                total_horas_trabajadas += jornada_ordinaria

                # Clasificar horas extra
                if es_domingo_o_festivo(dia):
                    horas_dominicales += horas_extra
                else:
                    # Simplificación: asumimos que si la salida es después de 21:00 (9 PM) son nocturnas
                    hora_salida = registros['salida'].hour
                    if hora_salida >= 21 or hora_salida < 6:
                        horas_extra_nocturnas += horas_extra
                    else:
                        horas_extra_diurnas += horas_extra
            else:
                total_horas_trabajadas += horas_dia

            dias_liquidados.add(dia)

    return {
        'horas_trabajadas': total_horas_trabajadas,
        'horas_extra_diurnas': horas_extra_diurnas,
        'horas_extra_nocturnas': horas_extra_nocturnas,
        'horas_dominicales': horas_dominicales,
        'dias_liquidados': len(dias_liquidados),
    }


def calcular_nomina_empleado(empleado, periodo_inicio, periodo_fin, user=None, request=None):
    """
    Calcula la liquidación de nómina completa para un empleado en un período.
    Aplica ajuste por SMMLV si el salario base del empleado es inferior al mínimo legal.

    Returns:
        dict con todos los valores calculados
    """
    salario_base_original = Decimal(str(empleado.salario_base))

    # Leer SMMLV desde parámetros del sistema y ajustar si es necesario
    try:
        smmlv_valor = Decimal(get_parametro('SMMLV', '1300606.00'))
    except Exception:
        smmlv_valor = Decimal('1300606.00')

    salario_base = salario_base_original
    if salario_base < smmlv_valor:
        salario_base = smmlv_valor

    valor_hora = calcular_valor_hora(salario_base)

    # Obtener horas del período
    horas = calcular_horas_extras(empleado, periodo_inicio, periodo_fin)

    # Calcular recargos
    recargo_diurno = (valor_hora * RECARGO_HORA_EXTRA_DIURNA * horas['horas_extra_diurnas']).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    recargo_nocturno = (valor_hora * RECARGO_HORA_EXTRA_NOCTURNA * horas['horas_extra_nocturnas']).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    recargo_dominical = Decimal('0')
    if horas['horas_dominicales'] > 0:
        recargo_dominical = (valor_hora * RECARGO_DOMINICAL_FESTIVO * horas['horas_dominicales']).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    # Total devengado
    total_devengado = (salario_base + recargo_diurno + recargo_nocturno + recargo_dominical).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    # Obtener porcentajes de parametrización
    try:
        pct_salud = Decimal(get_parametro('SALUD_APORTE', '4.0'))
        pct_pension = Decimal(get_parametro('PENSION_APORTE', '4.0'))
        pct_arl = Decimal(get_parametro('ARL_APORTE', '0.522'))
    except Exception:
        pct_salud = Decimal('4.0')
        pct_pension = Decimal('4.0')
        pct_arl = Decimal('0.522')

    # Deducciones
    descuento_salud = (total_devengado * pct_salud / Decimal('100')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    descuento_pension = (total_devengado * pct_pension / Decimal('100')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    descuento_arl = (salario_base * pct_arl / Decimal('100')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    total_deducciones = (descuento_salud + descuento_pension + descuento_arl).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    neto_pagar = (total_devengado - total_deducciones).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    return {
        'salario_base': salario_base,
        'salario_base_original': salario_base_original,
        'smmlv_aplicado': smmlv_valor,
        'valor_hora': valor_hora,
        'horas_trabajadas': horas['horas_trabajadas'],
        'horas_extra_diurnas': horas['horas_extra_diurnas'],
        'horas_extra_nocturnas': horas['horas_extra_nocturnas'],
        'horas_dominicales': horas['horas_dominicales'],
        'recargo_diurno': recargo_diurno,
        'recargo_nocturno': recargo_nocturno,
        'recargo_dominical': recargo_dominical,
        'total_devengado': total_devengado,
        'descuento_salud': descuento_salud,
        'descuento_pension': descuento_pension,
        'descuento_arl': descuento_arl,
        'total_deducciones': total_deducciones,
        'neto_pagar': neto_pagar,
        'dias_liquidados': horas['dias_liquidados'],
    }


def guardar_liquidacion(empleado, calculo, periodo_inicio, periodo_fin, user=None, request=None):
    """
    Guarda o actualiza la liquidación de nómina para un empleado en un período.
    """
    liquidacion, created = LiquidacionNomina.objects.update_or_create(
        empleado=empleado,
        periodo_inicio=periodo_inicio,
        periodo_fin=periodo_fin,
        defaults={
            'salario_base': calculo['salario_base'],
            'salario_base_original': calculo.get('salario_base_original'),
            'smmlv_aplicado': calculo.get('smmlv_aplicado'),
            'valor_hora': calculo['valor_hora'],
            'horas_trabajadas': calculo['horas_trabajadas'],
            'horas_extra_diurnas': calculo['horas_extra_diurnas'],
            'horas_extra_nocturnas': calculo['horas_extra_nocturnas'],
            'horas_dominicales': calculo['horas_dominicales'],
            'recargo_diurno': calculo['recargo_diurno'],
            'recargo_nocturno': calculo['recargo_nocturno'],
            'recargo_dominical': calculo['recargo_dominical'],
            'total_devengado': calculo['total_devengado'],
            'descuento_salud': calculo['descuento_salud'],
            'descuento_pension': calculo['descuento_pension'],
            'descuento_arl': calculo['descuento_arl'],
            'total_deducciones': calculo['total_deducciones'],
            'neto_pagar': calculo['neto_pagar'],
            'dias_liquidados': calculo['dias_liquidados'],
            'estado': 'LIQUIDADA' if calculo['dias_liquidados'] > 0 else 'CALCULADA',
        }
    )

    # Registrar en auditoría
    accion = 'CREAR_LIQUIDACION' if created else 'ACTUALIZAR_LIQUIDACION'
    registrar_auditoria(
        user, accion, 'liquidaciones_nomina', liquidacion.id,
        None if created else {'estado': 'CALCULADA'},
        {
            'empleado_id': empleado.id,
            'periodo': f"{periodo_inicio} a {periodo_fin}",
            'total_devengado': str(calculo['total_devengado']),
            'total_deducciones': str(calculo['total_deducciones']),
            'neto_pagar': str(calculo['neto_pagar']),
            'dias_liquidados': calculo['dias_liquidados'],
        },
        request
    )

    return liquidacion
