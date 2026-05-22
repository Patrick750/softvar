"""
Script de seed para poblar la base de datos con datos de prueba.
Uso: python manage.py seed_data [--force]

Crea:
- 3 administradores con diferentes roles
- 4 empleados de prueba
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from backend.empleados.models import Empleado
from datetime import date


ADMINS = [
    {
        "username": "admin_rrhh",
        "email": "rrhh@empresa.com",
        "password": "Admin123*",
        "first_name": "Carlos",
        "last_name": "Mendoza Lopez",
        "rol": "ADMIN_RRHH",
        "is_staff": True,
    },
    {
        "username": "contador",
        "email": "contador@empresa.com",
        "password": "Admin123*",
        "first_name": "Maria",
        "last_name": "Garcia Torres",
        "rol": "CONTADOR",
        "is_staff": True,
    },
    {
        "username": "gerente",
        "email": "gerente@empresa.com",
        "password": "Admin123*",
        "first_name": "Andres",
        "last_name": "Felipe Ramirez",
        "rol": "GERENTE",
        "is_staff": True,
    },
]

SAMPLE_EMPLOYEES = [
    {
        "cedula": "1001234567",
        "nombres": "Laura",
        "apellidos": "Cifuentes Pardo",
        "email": "laura.cifuentes@empresa.com",
        "telefono": "3101234567",
        "cargo": "Desarrollador Senior",
        "tipo_contrato": "TERMINO_INDEFINIDO",
        "salario_base": 4500000.00,
        "fecha_ingreso": date(2024, 3, 1),
        "eps": "Sanitas",
        "afp": "Porvenir",
        "arl": "Positiva",
    },
    {
        "cedula": "1002345678",
        "nombres": "Pedro",
        "apellidos": "Martinez Rojas",
        "email": "pedro.martinez@empresa.com",
        "telefono": "3112345678",
        "cargo": "Analista de Calidad",
        "tipo_contrato": "TERMINO_FIJO",
        "salario_base": 2800000.00,
        "fecha_ingreso": date(2024, 6, 15),
        "eps": "Nueva EPS",
        "afp": "Colfondos",
        "arl": "Sura",
    },
    {
        "cedula": "1003456789",
        "nombres": "Diana",
        "apellidos": "Alvarez Medina",
        "email": "diana.alvarez@empresa.com",
        "telefono": "3123456789",
        "cargo": "Disenadora UX/UI",
        "tipo_contrato": "PRESTACION_SERVICIOS",
        "salario_base": 3200000.00,
        "fecha_ingreso": date(2024, 1, 10),
        "eps": "Compensar",
        "afp": "Proteccion",
        "arl": "Bolivar",
    },
    {
        "cedula": "1004567890",
        "nombres": "Jorge",
        "apellidos": "Hernandez Sanchez",
        "email": "jorge.hernandez@empresa.com",
        "telefono": "3134567890",
        "cargo": "Scrum Master",
        "tipo_contrato": "TERMINO_INDEFINIDO",
        "salario_base": 5500000.00,
        "fecha_ingreso": date(2023, 9, 5),
        "eps": "Colsanitas",
        "afp": "Porvenir",
        "arl": "Positiva",
    },
]


class Command(BaseCommand):
    help = "Puebla la base de datos con administradores y empleados de prueba"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Elimina datos existentes y los recrea",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        if force:
            self.stdout.write(self.style.WARNING("[!] Modo --force: limpiando datos existentes..."))
            Empleado.objects.all().delete()
            User.objects.filter(is_superuser=False).exclude(
                username__in=["admin"]
            ).delete()
            Group.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("[OK] Datos anteriores eliminados"))

        self._create_admins()
        self._create_employees()

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("[OK] Seed completado exitosamente"))
        self.stdout.write("=" * 50)
        self._print_summary()

    def _create_admins(self):
        self.stdout.write("\n[+] Creando administradores...")
        created_count = 0

        for data in ADMINS:
            username = data["username"]
            email = data["email"]

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "password": make_password(data["password"]),
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": data["is_staff"],
                },
            )

            # Si el usuario ya existia pero no tiene el grupo, actualizamos contrasena
            if not created:
                user.password = make_password(data["password"])
                user.save()

            # Asignar grupo de rol
            group, _ = Group.objects.get_or_create(name=data["rol"])
            user.groups.add(group)

            if created:
                created_count += 1
                status = self.style.SUCCESS("[OK] Creado")
            else:
                status = self.style.WARNING("[~] Ya existe")

            self.stdout.write(
                f"  {status} | {data['rol']:15s} | {email:30s} | {data['password']}"
            )

        self.stdout.write(self.style.SUCCESS(f"  [OK] Total: {len(ADMINS)} usuarios ({created_count} nuevos)"))

    def _create_employees(self):
        self.stdout.write("\n[+] Creando empleados de prueba...")
        created_count = 0
        for data in SAMPLE_EMPLOYEES:
            _, created = Empleado.objects.get_or_create(
                cedula=data["cedula"],
                defaults=data,
            )
            if created:
                created_count += 1
                status = self.style.SUCCESS("[OK] Creado")
            else:
                status = self.style.WARNING("[~] Ya existe")

            self.stdout.write(
                f"  {status} | {data['cedula']:12s} | {data['nombres'] + ' ' + data['apellidos']:35s} | {data['cargo']}"
            )

        self.stdout.write(
            self.style.SUCCESS(f"  [OK] Total: {len(SAMPLE_EMPLOYEES)} empleados ({created_count} nuevos)")
        )

    def _print_summary(self):
        total_users = User.objects.count()
        total_employees = Empleado.objects.count()

        self.stdout.write("\n[+] Resumen:")
        self.stdout.write(f"    Usuarios del sistema: {total_users}")
        self.stdout.write(f"    Empleados registrados: {total_employees}")
        self.stdout.write("\n[+] Credenciales de acceso:\n")
        for adm in ADMINS:
            self.stdout.write(
                f"    * {adm['rol']:20s} -> {adm['email']:30s} / {adm['password']}"
            )
