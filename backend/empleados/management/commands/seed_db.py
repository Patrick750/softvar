"""
Comando de Django para alimentar (seed) la base de datos con datos de prueba realistas
para todos los modelos definidos en backend/empleados/models.py.

Uso:
  python manage.py seed_db           # Revisa y genera los registros faltantes
  python manage.py seed_db --force   # Elimina los datos de prueba y vuelve a generarlos
"""

import random
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from backend.empleados.models import (
    Empleado,
    ParametroSistema,
    Asistencia,
    Auditoria,
    Nomina,
    DetalleNomina
)


# Datos base para usuarios iniciales por rol
ROLES_CONFIG = [
    {
        "username": "admin_rrhh",
        "email": "rrhh@empresa.com",
        "password": "Admin123*",
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "rol": "ADMIN_RRHH",
        "cargo": "Administrador de RRHH",
        "cedula": "1018293847",
        "salario": Decimal("4500000.00"),
        "is_staff": True,
    },
    {
        "username": "contador",
        "email": "contador@empresa.com",
        "password": "Admin123*",
        "first_name": "María",
        "last_name": "García",
        "rol": "CONTADOR",
        "cargo": "Contador General",
        "cedula": "1029384756",
        "salario": Decimal("4200000.00"),
        "is_staff": True,
    },
    {
        "username": "gerente",
        "email": "gerente@empresa.com",
        "password": "Admin123*",
        "first_name": "Andrés",
        "last_name": "Ramírez",
        "rol": "GERENTE",
        "cargo": "Gerente General",
        "salario": Decimal("8500000.00"),
        "is_staff": True,
    },
    {
        "username": "admin_sistema",
        "email": "sistema@empresa.com",
        "password": "Admin123*",
        "first_name": "Laura",
        "last_name": "Torres",
        "rol": "ADMIN_SISTEMA",
        "cargo": "Administrador del Sistema",
        "cedula": "1047562938",
        "salario": Decimal("5000000.00"),
        "is_staff": True,
    },
    {
        "username": "empleado_demo",
        "email": "empleado@empresa.com",
        "password": "Empleado123*",
        "first_name": "Pedro",
        "last_name": "Martínez",
        "rol": "EMPLEADO",
        "cargo": "Analista de Desarrollo",
        "cedula": "1056473829",
        "salario": Decimal("2800000.00"),
        "is_staff": False,
    },
]

# Lista de empleados adicionales para robustecer el dataset
EMPLEADOS_ADICIONALES = [
    {
        "username": "jrodriguez",
        "email": "juan.rodriguez@empresa.com",
        "password": "Password123*",
        "first_name": "Juan",
        "last_name": "Rodríguez",
        "rol": "EMPLEADO",
        "cargo": "Desarrollador Senior",
        "cedula": "1098765432",
        "salario": Decimal("5500000.00"),
    },
    {
        "username": "mgomez",
        "email": "marta.gomez@empresa.com",
        "password": "Password123*",
        "first_name": "Marta",
        "last_name": "Gómez",
        "rol": "EMPLEADO",
        "cargo": "Diseñador UX/UI",
        "cedula": "1087654321",
        "salario": Decimal("3200000.00"),
    },
    {
        "username": "lhernandez",
        "email": "luis.hernandez@empresa.com",
        "password": "Password123*",
        "first_name": "Luis",
        "last_name": "Hernández",
        "rol": "EMPLEADO",
        "cargo": "Analista de Calidad",
        "cedula": "1076543210",
        "salario": Decimal("2600000.00"),
    },
    {
        "username": "sperez",
        "email": "sofia.perez@empresa.com",
        "password": "Password123*",
        "first_name": "Sofía",
        "last_name": "Pérez",
        "rol": "EMPLEADO",
        "cargo": "Scrum Master",
        "cedula": "1065432109",
        "salario": Decimal("4800000.00"),
    },
    {
        "username": "dcastro",
        "email": "diego.castro@empresa.com",
        "password": "Password123*",
        "first_name": "Diego",
        "last_name": "Castro",
        "rol": "EMPLEADO",
        "cargo": "Auxiliar Contable",
        "cedula": "1054321098",
        "salario": Decimal("1900000.00"),
    },
]

PARAMETROS_INICIALES = [
    {
        "clave": "SALARIO_MINIMO_VIGENTE",
        "valor": "1300000",
        "descripcion": "Salario mínimo mensual legal vigente (SMLV)",
    },
    {
        "clave": "AUXILIO_TRANSPORTE",
        "valor": "162000",
        "descripcion": "Auxilio de transporte vigente",
    },
    {
        "clave": "HORA_ENTRADA_OFICIAL",
        "valor": "08:00",
        "descripcion": "Hora oficial de entrada laboral",
    },
    {
        "clave": "HORA_SALIDA_OFICIAL",
        "valor": "17:00",
        "descripcion": "Hora oficial de salida laboral",
    },
    {
        "clave": "DESCUENTO_SALUD_PORCENTAJE",
        "valor": "4.0",
        "descripcion": "Porcentaje de descuento para salud",
    },
    {
        "clave": "DESCUENTO_PENSION_PORCENTAJE",
        "valor": "4.0",
        "descripcion": "Porcentaje de descuento para pensión",
    },
    {
        "clave": "MARGEN_TOLERANCIA_MINUTOS",
        "valor": "15",
        "descripcion": "Minutos de tolerancia de llegada tarde antes de sanción o reporte",
    },
    {
        "clave": "UMBRAL_RECONOCIMIENTO_FACIAL",
        "valor": "0.6",
        "descripcion": "Puntuación mínima de coincidencia para validación facial",
    },
]


class Command(BaseCommand):
    help = "Alimenta la base de datos con registros iniciales y de prueba para todos los modelos del sistema."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Limpia datos anteriores generados por el seed y vuelve a crearlos.",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        self.stdout.write(self.style.MIGRATE_HEADING("=== INICIANDO ALIMENTACIÓN DE LA BASE DE DATOS (SEED DB) ==="))

        if force:
            self._limpiar_datos()

        self._seed_parametros()
        users, empleados = self._seed_usuarios_y_empleados()
        self._seed_asistencias(empleados, users)
        self._seed_nominas(empleados)
        self._seed_auditorias(users)

        self.stdout.write(self.style.SUCCESS("\n[+] Base de datos alimentada exitosamente."))

    def _limpiar_datos(self):
        self.stdout.write(self.style.WARNING("[!] Modo --force activo: limpiando registros existentes..."))
        DetalleNomina.objects.all().delete()
        Nomina.objects.all().delete()
        Asistencia.objects.all().delete()
        Auditoria.objects.all().delete()
        ParametroSistema.objects.all().delete()
        
        all_usernames = [u["username"] for u in ROLES_CONFIG + EMPLEADOS_ADICIONALES]
        Empleado.objects.filter(user__username__in=all_usernames).delete()
        User.objects.filter(username__in=all_usernames).delete()
        self.stdout.write("  -> Registros anteriores eliminados satisfactoriamente.\n")

    def _seed_parametros(self):
        self.stdout.write(" -> Poblando Parámetros del Sistema...")
        creados = 0
        for item in PARAMETROS_INICIALES:
            obj, created = ParametroSistema.objects.get_or_create(
                clave=item["clave"],
                defaults={
                    "valor": item["valor"],
                    "descripcion": item["descripcion"],
                }
            )
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f"    OK: {creados} parámetros creados / procesados."))

    def _seed_usuarios_y_empleados(self):
        self.stdout.write(" -> Poblando Usuarios y Empleados...")
        eps_list = [c[0] for c in Empleado.EPS_CHOICES]
        afp_list = [c[0] for c in Empleado.AFP_CHOICES]
        arl_list = [c[0] for c in Empleado.ARL_CHOICES]
        banco_list = [c[0] for c in Empleado.BANCO_CHOICES]
        contrato_list = [c[0] for c in Empleado.TIPO_CONTRATO_CHOICES]

        created_users = []
        created_empleados = []

        all_user_data = ROLES_CONFIG + EMPLEADOS_ADICIONALES

        for idx, data in enumerate(all_user_data):
            username = data["username"]
            email = data["email"]
            rol = data["rol"]

            group, _ = Group.objects.get_or_create(name=rol)

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": data.get("is_staff", False),
                }
            )

            if user_created:
                user.set_password(data["password"])
                user.save()

            user.groups.add(group)
            created_users.append(user)

            # Empleado vinculación
            cedula = data.get("cedula", f"10900000{idx}")
            empleado, emp_created = Empleado.objects.get_or_create(
                user=user,
                defaults={
                    "cedula": cedula,
                    "nombres": data["first_name"],
                    "apellidos": data["last_name"],
                    "email": email,
                    "telefono": f"300{random.randint(1000007, 9999999)}",
                    "cargo": data["cargo"],
                    "tipo_contrato": random.choice(contrato_list),
                    "salario_base": data["salario"],
                    "fecha_ingreso": date(2023, random.randint(1, 12), random.randint(1, 28)),
                    "eps": random.choice(eps_list),
                    "afp": random.choice(afp_list),
                    "arl": random.choice(arl_list),
                    "cuenta_bancaria": f"123-{random.randint(100000, 999999)}-99",
                    "banco": random.choice(banco_list),
                    "tipo_cuenta": random.choice(["AHORROS", "CORRIENTE"]),
                    "foto_facial_registrada": True,
                    "activo": True,
                }
            )
            created_empleados.append(empleado)

        self.stdout.write(self.style.SUCCESS(f"    OK: {len(created_empleados)} empleados/usuarios listos."))
        return created_users, created_empleados

    def _seed_asistencias(self, empleados, users):
        self.stdout.write(" -> Poblando Registros de Asistencia...")
        admin_user = next((u for u in users if u.is_staff), users[0])
        asistencias_creadas = 0

        # Generar asistencias para los últimos 7 días
        hoy = timezone.now()
        for i in range(7):
            fecha_dia = hoy - timedelta(days=i)
            # Solo días laborables (lunes a viernes: weekday 0..4)
            if fecha_dia.weekday() > 4:
                continue

            for emp in empleados:
                # Registro de entrada (alrededor de las 8:00 AM, ej. entre 7:50 y 8:15)
                hora_base_entrada = fecha_dia.replace(hour=7, minute=50, second=0, microsecond=0)
                hora_entrada = hora_base_entrada + timedelta(minutes=random.randint(0, 25))
                asig_entrada, created = Asistencia.objects.get_or_create(
                    empleado=emp,
                    tipo="ENTRADA",
                    fecha_hora=hora_entrada,
                    defaults={
                        "estado": "EXITO",
                        "latitud": Decimal("4.609710"),
                        "longitud": Decimal("-74.081750"),
                        "verificacion_facial_score": Decimal("0.965"),
                        "liveness_score": Decimal("0.980"),
                        "liveness_validated": True,
                        "observaciones": "Ingreso registrado correctamente via Reconocimiento Facial",
                        "aprobado_por": admin_user,
                    }
                )
                if created:
                    asistencias_creadas += 1

                # Registro de salida (alrededor de las 5:00 PM, ej. entre 17:00 y 17:30)
                hora_base_salida = fecha_dia.replace(hour=17, minute=0, second=0, microsecond=0)
                hora_salida = hora_base_salida + timedelta(minutes=random.randint(0, 30))
                asig_salida, created = Asistencia.objects.get_or_create(
                    empleado=emp,
                    tipo="SALIDA",
                    fecha_hora=hora_salida,
                    defaults={
                        "estado": "EXITO",
                        "latitud": Decimal("4.609710"),
                        "longitud": Decimal("-74.081750"),
                        "verificacion_facial_score": Decimal("0.950"),
                        "liveness_score": Decimal("0.975"),
                        "liveness_validated": True,
                        "observaciones": "Salida registrada correctamente",
                        "aprobado_por": admin_user,
                    }
                )
                if created:
                    asistencias_creadas += 1

        self.stdout.write(self.style.SUCCESS(f"    OK: {asistencias_creadas} registros de asistencia creados."))

    def _seed_nominas(self, empleados):
        self.stdout.write(" -> Poblando Nóminas y Detalles de Nómina...")
        periodos = [
            (2026, 7),
            (2026, 8),
        ]

        for ano, mes in periodos:
            nomina, created = Nomina.objects.get_or_create(
                ano=ano,
                mes=mes,
                defaults={
                    "total_nomina": Decimal("0"),
                    "total_devengados": Decimal("0"),
                    "total_deducciones": Decimal("0"),
                }
            )

            total_dev = Decimal("0")
            total_ded = Decimal("0")

            for emp in empleados:
                salario = emp.salario_base
                hrs_extra_diurnas = random.randint(0, 5)
                hrs_extra_nocturnas = random.randint(0, 2)

                valor_hora = salario / Decimal("240")
                dev_extras = (Decimal(hrs_extra_diurnas) * valor_hora * Decimal("1.25")) + \
                             (Decimal(hrs_extra_nocturnas) * valor_hora * Decimal("1.75"))

                devengado_total = salario + dev_extras
                desc_salud = devengado_total * Decimal("0.04")
                desc_pension = devengado_total * Decimal("0.04")
                deducciones_total = desc_salud + desc_pension
                neto_pagar = devengado_total - deducciones_total

                DetalleNomina.objects.get_or_create(
                    nomina=nomina,
                    empleado=emp,
                    defaults={
                        "salario_base": salario,
                        "horas_extra_diurnas": hrs_extra_diurnas,
                        "horas_extra_nocturnas": hrs_extra_nocturnas,
                        "devengado_total": devengado_total,
                        "descuento_salud": desc_salud,
                        "descuento_pension": desc_pension,
                        "deducciones_total": deducciones_total,
                        "neto_pagar": neto_pagar,
                    }
                )

                total_dev += devengado_total
                total_ded += deducciones_total

            nomina.total_devengados = total_dev
            nomina.total_deducciones = total_ded
            nomina.total_nomina = total_dev - total_ded
            nomina.save()

        self.stdout.write(self.style.SUCCESS("    OK: Nóminas del periodo 2026/07 y 2026/08 liquidadas."))

    def _seed_auditorias(self, users):
        self.stdout.write(" -> Poblando Registros de Auditoría...")
        user_admin = users[0]
        acciones = [
            ("Empleado", "CREAR", "Creación inicial de datos de empleados"),
            ("Asistencia", "APROBAR_MANUAL", "Aprobación manual de asistencia con justificación"),
            ("Nomina", "MODIFICAR", "Cálculo y generación de la nómina del periodo"),
            ("User", "INICIO_SESION", "Inicio de sesión de usuario en el portal"),
        ]

        auditorias_creadas = 0
        for tabla, accion, desc in acciones:
            aud, created = Auditoria.objects.get_or_create(
                usuario=user_admin,
                tabla_afectada=tabla,
                accion=accion,
                defaults={
                    "registro_id": random.randint(1, 50),
                    "valor_anterior": "",
                    "valor_nuevo": f"Acción realizada: {desc}",
                    "ip_address": "127.0.0.1",
                }
            )
            if created:
                auditorias_creadas += 1

        self.stdout.write(self.style.SUCCESS(f"    OK: {auditorias_creadas} eventos de auditoría creados."))
