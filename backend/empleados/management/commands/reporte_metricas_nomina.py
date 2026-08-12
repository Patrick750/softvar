"""
Comando de Django para generar un reporte detallado de métricas para la liquidación de nómina.

Uso:
  python manage.py reporte_metricas_nomina                      # Mes y año actual
  python manage.py reporte_metricas_nomina --mes 8 --ano 2026    # Periodo específico
  python manage.py reporte_metricas_nomina --csv                # Exporta el reporte a archivo CSV
"""

import calendar
import csv
from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.empleados.models import Empleado, Asistencia, Nomina, DetalleNomina, ParametroSistema


class Command(BaseCommand):
    help = "Genera un reporte consolidado con las métricas necesarias para calcular la nómina de los empleados."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mes",
            type=int,
            default=timezone.now().month,
            help="Mes a consultar (1-12). Por defecto mes actual.",
        )
        parser.add_argument(
            "--ano",
            type=int,
            default=timezone.now().year,
            help="Año a consultar. Por defecto año actual.",
        )
        parser.add_argument(
            "--csv",
            action="store_true",
            help="Exportar el reporte a un archivo CSV en el directorio del proyecto.",
        )

    def handle(self, *args, **options):
        mes = options["mes"]
        ano = options["ano"]
        export_csv = options["csv"]

        if mes < 1 or mes > 12:
            self.stderr.write(self.style.ERROR("Error: El mes debe estar entre 1 y 12."))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n========================================================================================="))
        self.stdout.write(self.style.MIGRATE_HEADING(f"          REPORTE DE MÉTRICAS PARA CÁLCULO DE NÓMINA - PERIODO {mes:02d}/{ano}          "))
        self.stdout.write(self.style.MIGRATE_HEADING(f"=========================================================================================\n"))

        # Obtener parámetros del sistema
        smlv_param = ParametroSistema.objects.filter(clave="SALARIO_MINIMO_VIGENTE").first()
        aux_trans_param = ParametroSistema.objects.filter(clave="AUXILIO_TRANSPORTE").first()

        SMMLV = Decimal(smlv_param.valor) if smlv_param else Decimal("1300000.00")
        AUXILIO_TRANSPORTE = Decimal(aux_trans_param.valor) if aux_trans_param else Decimal("162000.00")

        # Calcular días hábiles del mes (Lunes a Viernes)
        _, num_days = calendar.monthrange(ano, mes)
        dias_habiles_mes = sum(1 for day in range(1, num_days + 1) if calendar.weekday(ano, mes, day) < 5)

        empleados = Empleado.objects.filter(activo=True).order_by("apellidos", "nombres")

        if not empleados.exists():
            self.stdout.write(self.style.WARNING("No se encontraron empleados activos en el sistema."))
            return

        # Verificar si ya existe una nómina procesada en BD para este periodo
        nomina_existente = Nomina.objects.filter(mes=mes, ano=ano).first()
        detalles_dict = {}
        if nomina_existente:
            for det in DetalleNomina.objects.filter(nomina=nomina_existente):
                detalles_dict[det.empleado_id] = det

        reporte_rows = []
        totales = {
            "salario_base": Decimal("0"),
            "devengado": Decimal("0"),
            "deducciones": Decimal("0"),
            "neto": Decimal("0"),
            "he_diurnas": 0,
            "he_nocturnas": 0,
            "dias_asistidos": 0,
            "faltas": 0
        }

        for emp in empleados:
            # Métricas de Asistencia
            asistencias_exito = Asistencia.objects.filter(
                empleado=emp,
                tipo="ENTRADA",
                estado="EXITO",
                fecha_hora__year=ano,
                fecha_hora__month=mes
            )

            dias_asistidos_set = {ast.fecha_hora.date() for ast in asistencias_exito if ast.fecha_hora.weekday() < 5}
            dias_asistidos_count = len(dias_asistidos_set)
            faltas = max(0, dias_habiles_mes - dias_asistidos_count)
            dias_a_pagar = max(0, 30 - faltas)

            # Si ya se procesó nómina, leemos horas extras guardadas; de lo contrario 0
            if emp.id in detalles_dict:
                det = detalles_dict[emp.id]
                he_diurnas = det.horas_extra_diurnas
                he_nocturnas = det.horas_extra_nocturnas
            else:
                he_diurnas = 0
                he_nocturnas = 0

            # Cálculos de nómina
            salario_base = emp.salario_base
            valor_hora = salario_base / Decimal("240.0")

            valor_he_d = Decimal(he_diurnas) * valor_hora * Decimal("1.25")
            valor_he_n = Decimal(he_nocturnas) * valor_hora * Decimal("1.75")

            salario_proporcional = (salario_base / Decimal("30.0")) * Decimal(dias_a_pagar)
            base_aportes = salario_proporcional + valor_he_d + valor_he_n

            auxilio_transporte_pagar = Decimal("0")
            if salario_base <= (SMMLV * Decimal("2.0")):
                auxilio_transporte_pagar = (AUXILIO_TRANSPORTE / Decimal("30.0")) * Decimal(dias_a_pagar)

            devengado = base_aportes + auxilio_transporte_pagar

            desc_salud = base_aportes * Decimal("0.04")
            desc_pension = base_aportes * Decimal("0.04")
            deducciones = desc_salud + desc_pension

            neto_pagar = devengado - deducciones

            row = {
                "id": emp.id,
                "cedula": emp.cedula,
                "nombre": f"{emp.nombres} {emp.apellidos}",
                "cargo": emp.cargo,
                "salario_base": salario_base,
                "dias_asistidos": dias_asistidos_count,
                "faltas": faltas,
                "dias_pagar": dias_a_pagar,
                "he_diurnas": he_diurnas,
                "he_nocturnas": he_nocturnas,
                "devengado": devengado,
                "deducciones": deducciones,
                "neto": neto_pagar,
            }
            reporte_rows.append(row)

            # Acumular totales
            totales["salario_base"] += salario_base
            totales["devengado"] += devengado
            totales["deducciones"] += deducciones
            totales["neto"] += neto_pagar
            totales["he_diurnas"] += he_diurnas
            totales["he_nocturnas"] += he_nocturnas
            totales["dias_asistidos"] += dias_asistidos_count
            totales["faltas"] += faltas

        # Imprimir Consola en formato Tabla
        self.stdout.write(f"Días Hábiles del Mes: {dias_habiles_mes} | SMLV: ${SMMLV:,.2f} | Aux. Transporte: ${AUXILIO_TRANSPORTE:,.2f}\n")
        self.stdout.write(f"{'CÉDULA':<12} | {'NOMBRE EMPLEADO':<22} | {'ASIST.':<6} | {'FALTAS':<6} | {'HE(D/N)':<7} | {'SALARIO BASE':<13} | {'DEVENGADO':<13} | {'DEDUCC.':<11} | {'NETO A PAGAR':<13}")
        self.stdout.write("-" * 125)

        for r in reporte_rows:
            he_str = f"{r['he_diurnas']}/{r['he_nocturnas']}"
            self.stdout.write(
                f"{r['cedula']:<12} | "
                f"{r['nombre'][:22]:<22} | "
                f"{r['dias_asistidos']:<6} | "
                f"{r['faltas']:<6} | "
                f"{he_str:<7} | "
                f"${r['salario_base']:>11,.0f} | "
                f"${r['devengado']:>11,.0f} | "
                f"${r['deducciones']:>9,.0f} | "
                f"${r['neto']:>11,.0f}"
            )

        self.stdout.write("-" * 125)
        self.stdout.write(
            f"{'TOTALES':<12} | "
            f"{f'{len(reporte_rows)} Empleados':<22} | "
            f"{totales['dias_asistidos']:<6} | "
            f"{totales['faltas']:<6} | "
            f"{f\"{totales['he_diurnas']}/{totales['he_nocturnas']}\":<7} | "
            f"${totales['salario_base']:>11,.0f} | "
            f"${totales['devengado']:>11,.0f} | "
            f"${totales['deducciones']:>9,.0f} | "
            f"${totales['neto']:>11,.0f}"
        )
        self.stdout.write("=" * 125 + "\n")

        # Exportar a CSV si se solicitó
        if export_csv:
            filename = f"reporte_metricas_nomina_{ano}_{mes:02d}.csv"
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID", "Cédula", "Empleado", "Cargo", "Salario Base",
                    "Días Asistidos", "Faltas", "Días Pagados",
                    "HE Diurnas", "HE Nocturnas", "Total Devengado",
                    "Total Deducciones", "Neto a Pagar"
                ])
                for r in reporte_rows:
                    writer.writerow([
                        r["id"], r["cedula"], r["nombre"], r["cargo"],
                        float(r["salario_base"]), r["dias_asistidos"], r["faltas"],
                        r["dias_pagar"], r["he_diurnas"], r["he_nocturnas"],
                        float(r["devengado"]), float(r["deducciones"]), float(r["neto"])
                    ])
            self.stdout.write(self.style.SUCCESS(f"[+] Reporte exportado a CSV exitosamente: {filename}"))
