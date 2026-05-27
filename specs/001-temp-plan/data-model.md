# Data Model: Sprint 4 - Reportes y Exportación

## Existing Entities (from modelo actual)

### Empleado
- id: AutoField (PK)
- user: OneToOneField(User)
- cedula: CharField(max_length=20, unique)
- nombres: CharField(max_length=100)
- apellidos: CharField(max_length=100)
- email: EmailField(max_length=150, unique)
- telefono: CharField(max_length=20, blank, null)
- cargo: CharField(max_length=100, choices)
- tipo_contrato: CharField(max_length=30, choices)
- salario_base: DecimalField(max_digits=10, decimal_places=2)
- fecha_ingreso: DateField
- fecha_retiro: DateField(blank, null)
- eps: CharField(max_length=100, choices)
- afp: CharField(max_length=100, choices)
- arl: CharField(max_length=100, choices)
- cuenta_bancaria: CharField(max_length=30, blank, null)
- banco: CharField(max_length=80, choices, blank, null)
- tipo_cuenta: CharField(max_length=20, choices, blank, null)
- foto_facial: TextField(blank, null)  # JSON descriptor base64
- foto_facial_registrada: BooleanField(default=False)
- activo: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add)
- updated_at: DateTimeField(auto_now)

### Asistencia
- id: AutoField (PK)
- empleado: ForeignKey(Empleado, on_delete=CASCADE, related_name='asistencias')
- fecha_hora: DateTimeField(auto_now_add)
- tipo: CharField(max_length=10, choices=[ENTRADA, SALIDA])
- estado: CharField(max_length=20, choices=[EXITO, FALLIDO, PENDIENTE_APROBACION, RECHAZADO, FRAUDE])
- latitud: DecimalField(max_digits=9, decimal_places=6, blank, null)
- longitud: DecimalField(max_digits=9, decimal_places=6, blank, null)
- justificacion_manual: TextField(blank, null)
- aprobado_por: ForeignKey(User, on_delete=SET_NULL, null, blank, related_name='asistencias_aprobadas')
- verificacion_facial_score: DecimalField(max_digits=4, decimal_places=3, blank, null)
- liveness_score: DecimalField(max_digits=4, decimal_places=3, blank, null)
- liveness_validated: BooleanField(default=False)
- observaciones: TextField(blank, null)

### LiquidacionNomina
- id: AutoField (PK)
- empleado: ForeignKey(Empleado, on_delete=CASCADE, related_name='liquidaciones')
- periodo_inicio: DateField
- periodo_fin: DateField
- salario_base: DecimalField(max_digits=12, decimal_places=2)
- valor_hora: DecimalField(max_digits=10, decimal_places=2)
- horas_trabajadas: DecimalField(max_digits=6, decimal_places=2, default=0)
- horas_extra_diurnas: DecimalField(max_digits=6, decimal_places=2, default=0)
- horas_extra_nocturnas: DecimalField(max_digits=6, decimal_places=2, default=0)
- horas_dominicales: DecimalField(max_digits=6, decimal_places=2, default=0)
- recargo_diurno: DecimalField(max_digits=12, decimal_places=2, default=0)
- recargo_nocturno: DecimalField(max_digits=12, decimal_places=2, default=0)
- recargo_dominical: DecimalField(max_digits=12, decimal_places=2, default=0)
- total_devengado: DecimalField(max_digits=12, decimal_places=2, default=0)
- descuento_salud: DecimalField(max_digits=10, decimal_places=2, default=0)
- descuento_pension: DecimalField(max_digits=10, decimal_places=2, default=0)
- descuento_arl: DecimalField(max_digits=10, decimal_places=2, default=0)
- total_deducciones: DecimalField(max_digits=12, decimal_places=2, default=0)
- neto_pagar: DecimalField(max_digits=12, decimal_places=2, default=0)
- dias_liquidados: IntegerField(default=0)
- estado: CharField(max_length=20, choices=[CALCULADA, LIQUIDADA, ANULADA], default='CALCULADA')
- created_at: DateTimeField(auto_now_add)
- updated_at: DateTimeField(auto_now)

### Desprendible
- id: AutoField (PK)
- liquidacion: ForeignKey(LiquidacionNomina, on_delete=CASCADE, related_name='desprendibles')
- empleado: ForeignKey(Empleado, on_delete=CASCADE, related_name='desprendibles')
- periodo: CharField(max_length=7, help_text='Formato YYYY-MM')
- archivo_pdf: TextField(blank, null, help_text='Contenido base64 del PDF')
- estado: CharField(max_length=20, choices=[GENERADO, ENVIADO, FALLIDO], default='GENERADO')
- fecha_generacion: DateTimeField(auto_now_add)
- fecha_envio: DateTimeField(blank, null)
- email_enviado_a: EmailField(max_length=254, blank, null)
- error_mensaje: TextField(blank, null)

### Auditoria
- id: AutoField (PK)
- usuario: ForeignKey(User, on_delete=SET_NULL, null, blank, related_name='auditorias')
- fecha_hora: DateTimeField(auto_now_add)
- tabla_afectada: CharField(max_length=100)
- registro_id: IntegerField(blank, null)
- accion: CharField(max_length=50) # CREAR, MODIFICAR, ELIMINAR, INICIO_SESION, INTENTO_FALLIDO, APROBAR_MANUAL
- valor_anterior: TextField(blank, null)
- valor_nuevo: TextField(blank, null)
- ip_address: GenericIPAddressField(blank, null)

### ParametroSistema
- id: AutoField (PK)
- clave: CharField(max_length=100, unique)
- valor: TextField()
- descripcion: CharField(max_length=255, blank, null)
- updated_at: DateTimeField(auto_now)

## New Entities for Sprint 4

### ReporteFiltros (for storing user report preferences)
- id: AutoField (PK)
- usuario: ForeignKey(User, on_delete=CASCADE)
- nombre: CharField(max_length=100)  # Nombre del filtro guardado
- tipo_reporte: CharField(max_length=50)  # asistencia, nomina, etc.
- fecha_inicio: DateField
- fecha_fin: DateField
- empleados: ManyToManyField(Empleado, blank=True)  # None = todos
- incluir_horas_extra: BooleanField(default=False)
- formato_exportacion: CharField(max_length=20, choices=[EXCEL, PDF, CSV], default='EXCEL')
- creado_en: DateTimeField(auto_now_add)
- actualizado_en: DateTimeField(auto_now)

### ReporteProgramado (for scheduled reports)
- id: AutoField (PK)
- usuario: ForeignKey(User, on_delete=CASCADE)
- nombre: CharField(max_length=100)
- tipo_reporte: CharField(max_length=50)
- frecuencia: CharField(max_length=20, choices=[DIARIO, SEMANAL, MENSUAL], default='MENSUAL')
- dia_semana: IntegerField(blank, null)  # 0-6 para semanal
- dia_mes: IntegerField(blank, null)  # 1-31 para mensual
- hora: TimeField
- activo: BooleanField(default=True)
- ultimo_envio: DateTimeField(blank, null)
- proximo_envio: DateTimeField
- creado_en: DateTimeField(auto_now_add)
- actualizado_en: DateTimeField(auto_now)

### ConfiguracionACH (bank-specific ACH format)
- id: AutoField (PK)
- banco: CharField(max_length=100)  # Nombre del banco
- formato_cuenta: CharField(max_length=30)  # Ej: "00123456789"
- formato_valor: CharField(max_length=20)  # Ej: "00000000012345" (15 dígitos)
- formato_nombre: CharField(max_length=30)  # Ej: "APELLIDOS NOMBRE          "
- delimiter: CharField(max_length=1, default=',')  # Campo delimitador
- longitud_linea: IntegerField(default=0)  # 0 = variable, >0 = fixed width
- activo: BooleanField(default=True)
- criado_en: DateTimeField(auto_now_add)
- actualizado_en: DateTimeField(auto_now)

## Relationships

### Existing relationships (maintained)
- Empleado <-one-> User (Django auth)
- Empleado ->many Asistencia
- Empleado ->many LiquidacionNomina
- LiquidacionNomina ->many Desprendible
- Asistencia <-many Auditoría (intentos fallidos, etc.)
- Usuario <-many Auditoría (usuarios que realizan acciones)

### New relationships for Sprint 4
- Usuario ->many ReporteFiltros
- Usuario ->many ReporteProgramado
- Banco (configuración) ->many ConfiguracionACH (un banco puede tener múltiples formatos según tipo de cuenta)

## Validation Rules

### ReporteFiltros
- nombre: requerido, único por usuario
- tipo_reporte: debe ser uno de los tipos válidos
- fecha_inicio <= fecha_fin
- Si se especifican empleados, deben pertenecer a la empresa y estar activos

### ReporteProgramado
- nombre: requerido, único por usuario
- frecuencia: determina qué campos son obligatorios
  - SEMANAL: requiere dia_semana (0-6)
  - MENSUAL: requiere dia_mes (1-28, 29, 30 o 31 según mes)
- hora: requerido
- activo: booleano

### ConfiguracionACH
- banco: requerido
- formato_cuenta: regex permitido (solo números y letras)
- formato_valor: regex permitido (solo números, posibles ceros a la izquierda)
- formato_nombre: longitud fija o máximo permitido
- delimiter: un solo carácter
- longitud_linea: si >0, validar que suma de longitudes de campos = longitud_linea

## State Transitions

### LiquidacionNomina
- CALCULADA -> LIQUIDADA (cuando se aprueba el pago)
- LIQUIDADA -> ANULADA (solo por admin con justificación)
- ANULADA -> (no transitions back)  # Historial integrity

### Desprendible
- GENERADO -> ENVIADO (cuando se envía email exitosamente)
- GENERADO -> FALLIDO (error en envío de email)
- ENVIADO -> (no transitions back)  # Historial
- FALLIDO -> GENERADO (reintento de envío)

## Indexes for Performance

### Asistencia
- idx_asistencia_empleado_fecha: (empleado_id, fecha_hora)  # Para reportes por rango
- idx_asistencia_fecha: (fecha_hora)  # Para reportes generales por fecha
- idx_asistencia_estado: (estado)  # Para filtros por estado

### LiquidacionNomina
- idx_liquidacion_empleado_periodo: (empleado_id, periodo_inicio, periodo_fin)  # Único ya definido
- idx_liquidacion_fecha: (periodo_fin)  # Para reportes por período
- idx_liquidacion_estado: (estado)  # Para filtros por estado

### ReporteFiltros
- idx_reportefiltros_usuario: (usuario_id)
- idx_reportefiltros_tipo: (tipo_reporte)

### ReporteProgramado
- idx_reportesprogramado_usuario: (usuario_id)
- idx_reportesprogramado_activo: (activo)  # Para jobs scheduler
- idx_reportesprogramado_proximo: (proximo_envio)  # Para evaluar qué ejecutar

### ConfiguracionACH
- idx_configach_banco: (banco)
- idx_configach_activo: (activo)