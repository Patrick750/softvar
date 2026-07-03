import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from empleados.models import Empleado, Asistencia, Nomina
from django.utils import timezone

try:
    empleados = Empleado.objects.filter(activo=True)
    if not empleados.exists():
        print("No empleados")
    
    nomina = Nomina.objects.create(mes=7, ano=2026)
    
    import calendar
    mes_int = 7
    ano_int = 2026
    
    _, num_days = calendar.monthrange(ano_int, mes_int)
    dias_habiles_mes = sum(1 for day in range(1, num_days + 1) if calendar.weekday(ano_int, mes_int, day) < 5)

    SMMLV = 1500000.0
    AUXILIO_TRANSPORTE = 180000.0

    for empleado in empleados:
        asistencias_exito = Asistencia.objects.filter(
            empleado=empleado,
            tipo='ENTRADA',
            estado='EXITO',
            fecha_hora__year=ano_int,
            fecha_hora__month=mes_int
        )
        dias_asistidos = set()
        for ast in asistencias_exito:
            if ast.fecha_hora.weekday() < 5:
                dias_asistidos.add(ast.fecha_hora.date())
        
        dias_asistidos_count = len(dias_asistidos)
        faltas = max(0, dias_habiles_mes - dias_asistidos_count)
        dias_a_pagar = max(0, 30 - faltas)
    print("Success")
    nomina.delete()
except Exception as e:
    import traceback
    traceback.print_exc()
