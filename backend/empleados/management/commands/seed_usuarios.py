"""
Comando para poblar la base de datos con 1 usuario por rol del sistema.

Uso:
  python manage.py seed_usuarios              # Crea solo si no existen
  python manage.py seed_usuarios --force      # Elimina y recrea todos

Roles creados:
  - ADMIN_RRHH      → rrhh@empresa.com       / Admin123*
  - CONTADOR        → contador@empresa.com   / Admin123*
  - GERENTE         → gerente@empresa.com    / Admin123*
  - ADMIN_SISTEMA   → sistema@empresa.com    / Admin123*
  - EMPLEADO        → empleado@empresa.com   / Empleado123*
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from backend.empleados.models import Empleado
from datetime import date

USERS_BY_ROLE = [
    {
        "username": "admin_rrhh",
        "email": "rrhh@empresa.com",
        "password": "Admin123*",
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "rol": "ADMIN_RRHH",
        "cargo": "Administrador de RRHH",
        "salario": 0,
        "is_staff": True,
    },
    {
        "username": "contador",
        "email": "contador@empresa.com",
        "password": "Admin123*",
        "first_name": "Maria",
        "last_name": "Garcia",
        "rol": "CONTADOR",
        "cargo": "Contador General",
        "salario": 0,
        "is_staff": True,
    },
    {
        "username": "gerente",
        "email": "gerente@empresa.com",
        "password": "Admin123*",
        "first_name": "Andres",
        "last_name": "Ramirez",
        "rol": "GERENTE",
        "cargo": "Gerente General",
        "salario": 0,
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
        "salario": 0,
        "is_staff": True,
    },
    {
        "username": "empleado_demo",
        "email": "empleado@empresa.com",
        "password": "Empleado123*",
        "first_name": "Pedro",
        "last_name": "Martinez",
        "rol": "EMPLEADO",
        "cargo": "Analista de Desarrollo",
        "salario": 2800000,
        "is_staff": False,
    },
]


class Command(BaseCommand):
    help = "Crea 1 usuario por rol del sistema (ADMIN_RRHH, CONTADOR, GERENTE, ADMIN_SISTEMA, EMPLEADO)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Elimina los usuarios creados por este seed y los recrea",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        if force:
            self._clean_existing()

        created_users = []
        skipped_users = []

        for data in USERS_BY_ROLE:
            result = self._create_user(data)
            if result == "created":
                created_users.append(data["rol"])
            else:
                skipped_users.append(data["rol"])

        self._print_summary(created_users, skipped_users)

    def _clean_existing(self):
        self.stdout.write(self.style.WARNING("[!] Modo --force: eliminando usuarios del seed..."))
        usernames = [u["username"] for u in USERS_BY_ROLE]

        # Eliminar empleados asociados
        Empleado.objects.filter(user__username__in=usernames).delete()
        self.stdout.write("  -> Empleados eliminados")

        # Eliminar usuarios
        deleted, _ = User.objects.filter(username__in=usernames).delete()
        self.stdout.write(f"  -> {deleted} usuarios eliminados")

        # No eliminamos los grupos porque pueden estar en uso por otros datos
        self.stdout.write(self.style.SUCCESS("[OK] Limpieza completada\n"))

    def _create_user(self, data):
        username = data["username"]
        email = data["email"]
        rol = data["rol"]

        # Verificar si ya existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Asegurar grupo y contraseña
            group, _ = Group.objects.get_or_create(name=rol)
            user.groups.add(group)
            user.set_password(data["password"])
            user.save()
            self._ensure_empleado_profile(user, data)
            return "skipped"

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            is_staff=data["is_staff"],
        )

        # Asignar grupo de rol
        group, _ = Group.objects.get_or_create(name=rol)
        user.groups.add(group)

        # Crear perfil de Empleado (necesario para acceder al Portal Personal)
        self._ensure_empleado_profile(user, data)

        return "created"

    def _ensure_empleado_profile(self, user, data):
        """Crea el perfil Empleado si el usuario no tiene uno."""
        try:
            user.empleado
        except Empleado.DoesNotExist:
            Empleado.objects.create(
                user=user,
                cedula=user.username.upper()[:20],
                nombres=data["first_name"],
                apellidos=data["last_name"],
                email=data["email"],
                cargo=data["cargo"],
                tipo_contrato="TERMINO_INDEFINIDO",
                salario_base=data.get("salario", 0),
                fecha_ingreso=date.today(),
                eps="N/A",
                afp="N/A",
                arl="N/A",
                activo=True,
            )

    def _print_summary(self, created, skipped):
        self.stdout.write("\n" + "=" * 55)
        self.stdout.write(self.style.SUCCESS("RESUMEN — Seed de Usuarios"))
        self.stdout.write("=" * 55)

        for data in USERS_BY_ROLE:
            status = self.style.SUCCESS("[OK] Creado") if data["rol"] in created else self.style.WARNING("[~] Ya existe")
            self.stdout.write(f"  {status} | {data['rol']:15s} | {data['email']:28s} | {data['password']}")

        self.stdout.write("")
        self.stdout.write(f"  Creados: {len(created)} | Omitidos: {len(skipped)}")
        self.stdout.write("=" * 55)
        self.stdout.write("")
