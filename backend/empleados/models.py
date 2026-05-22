from django.db import models
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empleado')
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


class ParametroSistema(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametros_sistema'

    def __str__(self):
        return f"{self.clave}: {self.valor}"


class Asistencia(models.Model):
    TIPO_REGISTRO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    ESTADO_CHOICES = [
        ('EXITO', 'Exitoso'),
        ('FALLIDO', 'Fallido'),
        ('PENDIENTE_APROBACION', 'Pendiente de Aprobación'),
        ('RECHAZADO', 'Rechazado'),
    ]

    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asistencias')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPO_REGISTRO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EXITO')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    justificacion_manual = models.TextField(blank=True, null=True)
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asistencias_aprobadas')
    verificacion_facial_score = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'asistencias'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.empleado} - {self.tipo} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M') if self.fecha_hora else ''}"


class Auditoria(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tabla_afectada = models.CharField(max_length=100)
    registro_id = models.IntegerField(blank=True, null=True)
    accion = models.CharField(max_length=50) # CREAR, MODIFICAR, ELIMINAR, INICIO_SESION, INTENTO_FALLIDO, APROBAR_MANUAL
    valor_anterior = models.TextField(blank=True, null=True)
    valor_nuevo = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = 'auditoria'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.accion} on {self.tabla_afectada} by {self.usuario or 'System'} at {self.fecha_hora}"