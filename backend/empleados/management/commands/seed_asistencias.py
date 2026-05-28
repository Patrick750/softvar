"""
Comando para poblar la base de datos con registros de asistencia realistas.

Genera asistencias (ENTRADA/SALIDA) para todos los empleados con salario > 0,
para meses pasados completos, con horarios variados que incluyen horas extra.

Por defecto genera los últimos 3 meses completos (febrero, marzo, abril 2026).

Uso:
  python manage.py seed_asistencias                        # Crea para últimos 3 meses
  python manage.py seed_asistencias --force                # Elimina y recrea todo
  python manage.py seed_asistencias --force --mes=4        # Especificar mes (1-12)
  python manage.py seed_asistencias --force --anio=2026    # Especificar año
  python manage.py seed_asistencias --force --meses=3      # Generar los últimos N meses
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, datetime
from decimal import Decimal
import random
import calendar
from backend.empleados.models import Empleado, Asistencia

# Oficina coordenadas (Neiva, Huila)
OFICINA_LAT = Decimal('2.9273')
OFICINA_LON = Decimal('-75.2819')

# Perfiles de horario por empleado (según cargo)
PERFILES_HORARIO = {
    'Desarrollador Senior': {
        'entrada_min': (7, 0), 'entrada_max': (8, 30),
        'salida_min': (17, 0), 'salida_max': (19, 0),
        'prob_extra': 0.4,  # 40% de días con 1-3h extra
    },
    'Desarrollador Junior': {
        'entrada_min': (7, 30), 'entrada_max': (8, 30),
        'salida_min': (17, 0), 'salida_max': (18, 30),
        'prob_extra': 0.3,
    },
    'Analista de Calidad': {
        'entrada_min': (7, 0), 'entrada_max': (8, 0),
        'salida_min': (16, 0), 'salida_max': (17, 30),
        'prob_extra': 0.2,
    },
    'Analista de Desarrollo': {
        'entrada_min': (7, 30), 'entrada_max': (8, 30),
        'salida_min': (17, 0), 'salida_max': (18, 30),
        'prob_extra': 0.35,
    },
    'Diseñador UX/UI': {
        'entrada_min': (8, 0), 'entrada_max': (9, 0),
        'salida_min': (17, 0), 'salida_max': (18, 0),
        'prob_extra': 0.2,
    },
    'Scrum Master': {
        'entrada_min': (7, 0), 'entrada_max': (8, 0),
        'salida_min': (16, 30), 'salida_max': (18, 0),
        'prob_extra': 0.3,
    },
    'Product Owner': {
        'entrada_min': (7, 30), 'entrada_max': (8, 30),
        'salida_min': (16, 0), 'salida_max': (18, 0),
        'prob_extra': 0.25,
    },
    'Administrador de RRHH': {
        'entrada_min': (7, 30), 'entrada_max': (8, 30),
        'salida_min': (17, 0), 'salida_max': (18, 0),
        'prob_extra': 0.15,
    },
    'Contador General': {
        'entrada_min': (7, 0), 'entrada_max': (8, 0),
        'salida_min': (17, 0), 'salida_max': (19, 0),
        'prob_extra': 0.3,  # Más horas extra en cierre de mes
    },
    'Gerente General': {
        'entrada_min': (7, 30), 'entrada_max': (9, 0),
        'salida_min': (16, 0), 'salida_max': (17, 30),
        'prob_extra': 0.1,
    },
    'Auxiliar Contable': {
        'entrada_min': (7, 0), 'entrada_max': (8, 0),
        'salida_min': (16, 0), 'salida_max': (17, 30),
        'prob_extra': 0.2,
    },
    'Secretario(a)': {
        'entrada_min': (7, 30), 'entrada_max': (8, 30),
        'salida_min': (16, 0), 'salida_max': (17, 0),
        'prob_extra': 0.1,
    },
    'Practicante': {
        'entrada_min': (7, 0), 'entrada_max': (8, 0),
        'salida_min': (16, 0), 'salida_max': (17, 0),
        'prob_extra': 0.05,
    },
    'Administrador del Sistema': {
        'entrada_min': (7, 0), 'entrada_max': (8, 30),
        'salida_min': (16, 30), 'salida_max': (18, 0),
        'prob_extra': 0.25,
    },
}

# Perfil por defecto si el cargo no está listado
PERFIL_DEFECTO = {
    'entrada_min': (7, 30), 'entrada_max': (8, 30),
    'salida_min': (17, 0), 'salida_max': (17, 30),
    'prob_extra': 0.2,
}


def generar_hora_aleatoria(h_min, h_max):
    """Genera una hora aleatoria entre dos tuplas (hora, minuto)."""
    min_total = h_min[0] * 60 + h_min[1]
    max_total = h_max[0] * 60 + h_max[1]
    if max_total <= min_total:
        return h_min
    aleatorio = random.randint(min_total, max_total)
    return time(aleatorio // 60, aleatorio % 60)


def generar_minutos_extra(salida_base, salida_max):
    """
    Decide aleatoriamente si agregar horas extra y cuántas.
    Retorna la hora de salida final.
    """
    base_h = salida_base.hour
    base_m = salida_base.minute
    max_total = salida_max[0] * 60 + salida_max[1]
    base_total = base_h * 60 + base_m

    # Generar 1-3 horas extra (60-180 minutos adicionales)
    extra = random.randint(60, 180)
    final_total = min(base_total + extra, max_total)
    return time(final_total // 60, final_total % 60)


class Command(BaseCommand):
    help = "Puebla la base de datos con registros de asistencia realistas para testing de nómina"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Elimina las asistencias existentes y las recrea",
        )
        parser.add_argument(
            "--mes",
            type=int,
            default=0,
            help="Mes para generar asistencias (1-12). Por defecto: últimos 3 meses completos",
        )
        parser.add_argument(
            "--anio",
            type=int,
            default=2026,
            help="Año para generar asistencias (por defecto 2026)",
        )
        parser.add_argument(
            "--meses",
            type=int,
            default=3,
            help="Cantidad de meses pasados completos a generar (por defecto 3)",
        )
        parser.add_argument(
            "--empleados",
            type=str,
            default="",
            help="IDs de empleados separados por coma (e.g. '27,28,29'). Si se omite, usa todos con salario > 0",
        )

    def _calcular_meses_pasados(self, cantidad):
        """
        Calcula los últimos N meses completos.
        Retorna lista de tuplas (mes, anio) desde el más antiguo al más reciente.
        """
        hoy = timezone.now().date()
        # El mes actual no está completo, usamos el mes anterior
        mes_actual = hoy.month
        anio_actual = hoy.year

        meses = []
        for i in range(cantidad):
            # Retroceder i+1 meses desde el actual (el primero es el mes pasado)
            m = mes_actual - (i + 1)
            a = anio_actual
            while m < 1:
                m += 12
                a -= 1
            meses.append((m, a))

        # Ordenar del más antiguo al más reciente
        meses.reverse()
        return meses

    def handle(self, *args, **options):
        force = options.get("force", False)
        mes_especifico = options.get("mes", 0)
        anio = options.get("anio", 2026)
        meses_a_generar = options.get("meses", 3)
        empleados_ids_str = options.get("empleados", "")

        # Determinar meses a procesar
        if mes_especifico:
            periodos = [(mes_especifico, anio)]
        else:
            periodos = self._calcular_meses_pasados(meses_a_generar)

        # Determinar empleados objetivo
        if empleados_ids_str:
            ids = [int(x.strip()) for x in empleados_ids_str.split(",") if x.strip()]
            empleados = Empleado.objects.filter(id__in=ids, activo=True)
            if not empleados.exists():
                self.stdout.write(self.style.ERROR(f"No se encontraron empleados con IDs: {empleados_ids_str}"))
                return
        else:
            empleados = Empleado.objects.filter(salario_base__gt=0, activo=True)
            if not empleados.exists():
                self.stdout.write(self.style.WARNING(
                    "No hay empleados con salario > 0. Se usarán todos los empleados activos."
                ))
                empleados = Empleado.objects.filter(activo=True)

        if not empleados.exists():
            self.stdout.write(self.style.ERROR("No hay empleados activos en el sistema."))
            return

        # Si force, limpiar TODOS los periodos
        if force:
            for mes, anio_periodo in periodos:
                self._limpiar_asistencias(mes, anio_periodo)

        # Procesar cada periodo
        total_creadas = 0
        total_dias = 0

        for mes, anio_periodo in periodos:
            self.stdout.write(f"\nGenerando asistencias para {empleados.count()} empleados...")
            self.stdout.write(f"Período: {mes}/{anio_periodo}")
            self.stdout.write("-" * 50)

            resumen_por_empleado = []

            for empleado in empleados:
                perfil = PERFILES_HORARIO.get(empleado.cargo, PERFIL_DEFECTO)
                creadas = self._generar_asistencias_empleado(empleado, mes, anio_periodo, perfil)
                total_creadas += creadas["total"]
                total_dias += creadas["dias"]
                resumen_por_empleado.append(creadas)

            self.stdout.write(self.style.SUCCESS(f"\nRESUMEN — {mes}/{anio_periodo}"))
            for r in resumen_por_empleado:
                self.stdout.write(
                    f"  {r['empleado_nombre']:25s} | "
                    f"{r['cargo']:22s} | "
                    f"{r['dias']:2d} días | "
                    f"{r['extras']:2d} HE | "
                    f"{r['total']:3d} regs"
                )

        self.stdout.write("\n" + "=" * 55)
        self.stdout.write(self.style.SUCCESS("RESUMEN GLOBAL — Seed de Asistencias"))
        self.stdout.write("=" * 55)
        self.stdout.write(f"  Periodos generados: {len(periodos)}")
        self.stdout.write(f"  Total registros creados: {total_creadas}")
        self.stdout.write(f"  Total días-hombre: {total_dias}")
        for mes_p, anio_p in periodos:
            self.stdout.write(f"    - {mes_p:02d}/{anio_p}")
        self.stdout.write("=" * 55)

    def _limpiar_asistencias(self, mes, anio):
        """Elimina asistencias del mes/año especificado."""
        inicio = date(anio, mes, 1)
        if mes == 12:
            fin = date(anio + 1, 1, 1)
        else:
            fin = date(anio, mes + 1, 1)

        eliminadas, _ = Asistencia.objects.filter(
            fecha_hora__date__gte=inicio,
            fecha_hora__date__lt=fin,
        ).delete()
        self.stdout.write(self.style.WARNING(
            f"  -> {eliminadas} asistencias eliminadas del período {mes}/{anio}"
        ))

    def _es_festivo_colombia(self, fecha):
        """
        Festivos Colombia 2026 (simplificado — los principales).
        En producción se integraría con una API real.
        """
        festivos_2026 = [
            date(2026, 1, 1),   # Año Nuevo
            date(2026, 1, 12),  # Reyes Magos
            date(2026, 3, 23),  # San José
            date(2026, 3, 29),  # Domingo de Ramos
            date(2026, 4, 2),   # Jueves Santo
            date(2026, 4, 3),   # Viernes Santo
            date(2026, 4, 5),   # Domingo de Resurrección
            date(2026, 5, 1),   # Día del Trabajo
            date(2026, 5, 25),  # Ascensión de Jesús
            date(2026, 6, 15),  # Corpus Christi
            date(2026, 6, 22),  # Sagrado Corazón
            date(2026, 7, 20),  # Independencia
            date(2026, 8, 7),   # Batalla de Boyacá
            date(2026, 8, 17),  # Asunción
            date(2026, 10, 12), # Día de la Raza
            date(2026, 11, 2),  # Todos los Santos
            date(2026, 11, 16), # Independencia de Cartagena
            date(2026, 12, 8),  # Inmaculada Concepción
            date(2026, 12, 25), # Navidad
        ]
        return fecha in festivos_2026

    def _generar_asistencias_empleado(self, empleado, mes, anio, perfil):
        """
        Genera asistencias (ENTRADA + SALIDA) para un empleado en todo el mes.
        """
        if mes == 12:
            ultimo_dia = 31
        else:
            ultimo_dia = calendar.monthrange(anio, mes)[1]

        creadas = 0
        dias_trabajados = 0
        dias_con_extra = 0

        for dia in range(1, ultimo_dia + 1):
            fecha = date(anio, mes, dia)

            # Fines de semana y festivos → NO se trabaja (excepto algunas excepciones)
            es_finde = fecha.weekday() >= 5  # Sábado=5, Domingo=6
            es_festivo = self._es_festivo_colombia(fecha)

            if es_finde or es_festivo:
                # Probabilidad baja de trabajar en fin de semana/festivo (10%)
                if random.random() > 0.08:
                    continue

            # Probabilidad de ausencia (5% - el empleado falta ese día)
            if random.random() < 0.05 and dias_trabajados > 0:
                continue  # No tan seguido al inicio

            # Generar hora de entrada y salida base
            hora_entrada = generar_hora_aleatoria(
                perfil['entrada_min'], perfil['entrada_max']
            )
            hora_salida = generar_hora_aleatoria(
                perfil['salida_min'], perfil['salida_max']
            )

            # ¿Aplica horas extra hoy?
            tiene_extra = random.random() < perfil['prob_extra']
            if tiene_extra:
                hora_salida = generar_minutos_extra(hora_salida, (21, 0))
                dias_con_extra += 1

            # Pequeña variación de geolocalización (oficina)
            lat = OFICINA_LAT + Decimal(str(round(random.uniform(-0.002, 0.002), 6)))
            lon = OFICINA_LON + Decimal(str(round(random.uniform(-0.002, 0.002), 6)))

            # Score facial aleatorio (entre 0.85 y 1.0, siempre exitoso)
            facial_score = Decimal(str(round(random.uniform(0.88, 0.99), 3)))

            # Crear ENTRADA
            dt_entrada = timezone.make_aware(datetime.combine(fecha, hora_entrada))
            Asistencia.objects.create(
                empleado=empleado,
                fecha_hora=dt_entrada,
                tipo='ENTRADA',
                estado='EXITO',
                latitud=lat,
                longitud=lon,
                verificacion_facial_score=facial_score,
                liveness_score=Decimal(str(round(random.uniform(0.90, 1.0), 3))),
                liveness_validated=True,
            )
            creadas += 1

            # Crear SALIDA
            dt_salida = timezone.make_aware(datetime.combine(fecha, hora_salida))
            Asistencia.objects.create(
                empleado=empleado,
                fecha_hora=dt_salida,
                tipo='SALIDA',
                estado='EXITO',
                latitud=lat,
                longitud=lon,
                verificacion_facial_score=facial_score,
                liveness_score=Decimal(str(round(random.uniform(0.90, 1.0), 3))),
                liveness_validated=True,
            )
            creadas += 1
            dias_trabajados += 1

            # Ocasionalmente, un registro manual (sin biometría) para el admin
            # 3% de probabilidad de tener un registro PENDIENTE_APROBACION
            if random.random() < 0.03:
                dt_manual = timezone.make_aware(datetime.combine(fecha, time(14, 0)))
                Asistencia.objects.create(
                    empleado=empleado,
                    fecha_hora=dt_manual,
                    tipo='ENTRADA',
                    estado='PENDIENTE_APROBACION',
                    latitud=None,
                    longitud=None,
                    verificacion_facial_score=None,
                    liveness_score=None,
                    liveness_validated=False,
                    justificacion_manual="Registro manual por falla del sistema biométrico",
                )
                creadas += 1

        return {
            'empleado_nombre': f"{empleado.nombres} {empleado.apellidos}",
            'cargo': empleado.cargo,
            'dias': dias_trabajados,
            'extras': dias_con_extra,
            'total': creadas,
        }
