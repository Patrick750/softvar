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
    CARGO_CHOICES = [
        ('Desarrollador Senior', 'Desarrollador Senior'),
        ('Desarrollador Junior', 'Desarrollador Junior'),
        ('Analista de Calidad', 'Analista de Calidad'),
        ('Analista de Desarrollo', 'Analista de Desarrollo'),
        ('Diseñador UX/UI', 'Diseñador UX/UI'),
        ('Scrum Master', 'Scrum Master'),
        ('Product Owner', 'Product Owner'),
        ('Administrador de RRHH', 'Administrador de RRHH'),
        ('Contador General', 'Contador General'),
        ('Gerente General', 'Gerente General'),
        ('Administrador del Sistema', 'Administrador del Sistema'),
        ('Auxiliar Contable', 'Auxiliar Contable'),
        ('Secretario(a)', 'Secretario(a)'),
        ('Practicante', 'Practicante'),
    ]
    EPS_CHOICES = [
        ('Sanitas', 'Sanitas'),
        ('Nueva EPS', 'Nueva EPS'),
        ('Compensar', 'Compensar'),
        ('Colsanitas', 'Colsanitas'),
        ('Sura', 'Sura'),
        ('Salud Total', 'Salud Total'),
        ('Coomeva', 'Coomeva'),
        ('Famisanar', 'Famisanar'),
        ('Cafam', 'Cafam'),
        ('Cruz Blanca', 'Cruz Blanca'),
        ('Capital Salud', 'Capital Salud'),
        ('Mutual Ser', 'Mutual Ser'),
        ('Comfamiliar', 'Comfamiliar'),
    ]
    AFP_CHOICES = [
        ('Porvenir', 'Porvenir'),
        ('Colfondos', 'Colfondos'),
        ('Protección', 'Protección'),
        ('Old Mutual', 'Old Mutual'),
        ('Skandia', 'Skandia'),
    ]
    ARL_CHOICES = [
        ('Positiva', 'Positiva'),
        ('Sura', 'Sura'),
        ('Bolívar', 'Bolívar'),
        ('Colpatria', 'Colpatria'),
        ('Mapfre', 'Mapfre'),
        ('Colmena', 'Colmena'),
        ('Equidad', 'Equidad'),
        ('Aurora', 'Aurora'),
        ('Seguros del Estado', 'Seguros del Estado'),
    ]
    BANCO_CHOICES = [
        ('Bancolombia', 'Bancolombia'),
        ('Davivienda', 'Davivienda'),
        ('Banco de Bogotá', 'Banco de Bogotá'),
        ('Banco Popular', 'Banco Popular'),
        ('Banco de Occidente', 'Banco de Occidente'),
        ('BBVA', 'BBVA'),
        ('Colpatria', 'Colpatria'),
        ('AV Villas', 'AV Villas'),
        ('Itaú', 'Itaú'),
        ('Banco Agrario', 'Banco Agrario'),
        ('Bancoomeva', 'Bancoomeva'),
        ('Scotiabank Colpatria', 'Scotiabank Colpatria'),
        ('Banco Caja Social', 'Banco Caja Social'),
        ('Nequi', 'Nequi'),
        ('DaviPlata', 'DaviPlata'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empleado')
    cedula = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, choices=CARGO_CHOICES)
    tipo_contrato = models.CharField(max_length=30, choices=TIPO_CONTRATO_CHOICES)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    fecha_retiro = models.DateField(blank=True, null=True)
    eps = models.CharField(max_length=100, choices=EPS_CHOICES)
    afp = models.CharField(max_length=100, choices=AFP_CHOICES)
    arl = models.CharField(max_length=100, choices=ARL_CHOICES)
    cuenta_bancaria = models.CharField(max_length=30, blank=True, null=True)
    banco = models.CharField(max_length=80, choices=BANCO_CHOICES, blank=True, null=True)
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
        ('FRAUDE', 'Intento de fraude'),
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
    liveness_score = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, help_text='Puntuación de detección de vitalidad (0-1)')
    liveness_validated = models.BooleanField(default=False, help_text='Indica si pasó la validación de vitalidad')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'asistencias'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.empleado} - {self.tipo} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M') if self.fecha_hora else ''}"


class LiquidacionNomina(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='liquidaciones')
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    salario_base = models.DecimalField(max_digits=12, decimal_places=2)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    horas_trabajadas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    horas_extra_diurnas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    horas_extra_nocturnas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    horas_dominicales = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    recargo_diurno = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recargo_nocturno = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recargo_dominical = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_devengado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_salud = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento_pension = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento_arl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deducciones = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neto_pagar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dias_liquidados = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=[
        ('CALCULADA', 'Calculada'),
        ('LIQUIDADA', 'Liquidada'),
        ('ANULADA', 'Anulada'),
    ], default='CALCULADA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'liquidaciones_nomina'
        unique_together = ['empleado', 'periodo_inicio', 'periodo_fin']
        ordering = ['-periodo_fin', 'empleado__apellidos']

    def __str__(self):
        return f"{self.empleado} - {self.periodo_inicio} a {self.periodo_fin}"


class Desprendible(models.Model):
    id = models.AutoField(primary_key=True)
    liquidacion = models.ForeignKey(LiquidacionNomina, on_delete=models.CASCADE, related_name='desprendibles')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='desprendibles')
    periodo = models.CharField(max_length=7, help_text='Formato YYYY-MM')
    archivo_pdf = models.TextField(blank=True, null=True, help_text='Contenido base64 del PDF')
    estado = models.CharField(max_length=20, choices=[
        ('GENERADO', 'Generado'),
        ('ENVIADO', 'Enviado'),
        ('FALLIDO', 'Fallido'),
    ], default='GENERADO')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    email_enviado_a = models.EmailField(max_length=254, blank=True, null=True)
    error_mensaje = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'desprendibles'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f"Desprendible {self.empleado} - {self.periodo}"


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