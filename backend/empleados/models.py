from django.db import models

class Empleado(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('TERMINO_FIJO', 'Término Fijo'),
        ('TERMINO_INDEFINIDO', 'Término Indefinido'),
        ('OBRA_LABOR', 'Obra Labor'),
        ('PRESTACION_SERVICIOS', 'Prestación de Servicios'),
    ]
    TIPO_CUENTA_CHOICES = [
        ('AHORROS', 'Ahorros'),
        ('CORRIENTE', 'Corriente'),
    ]

    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100)
    tipo_contrato = models.CharField(max_length=30, choices=TIPO_CONTRATO_CHOICES)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    fecha_retiro = models.DateField(blank=True, null=True)
    eps = models.CharField(max_length=100)
    afp = models.CharField(max_length=100)
    arl = models.CharField(max_length=100)
    cuenta_bancaria = models.CharField(max_length=30, blank=True, null=True)
    banco = models.CharField(max_length=80, blank=True, null=True)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, blank=True, null=True)
    foto_facial = models.TextField(blank=True, null=True)  # JSON descriptor base64
    foto_facial_registrada = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empleados'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"