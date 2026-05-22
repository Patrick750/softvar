# Diseño Sprint 3: Liquidación de nómina, Desprendibles PDF, Parametrización SMMLV

## Enfoque elegido
Modular: apps Django separadas con APIs claras.

## Arquitectura
- `empleados_nomina`: Motor de cálculo de nómina.
- `empleados_desprendibles`: Generación de PDF y envío de emails masivos.
- `empleados_parametros`: Panel de actualización de parámetros SMMLV e historial.

## Flujo de datos
1. Los registros de asistencia (sprint 2) proveen las horas trabajadas como base para la liquidación de nómina.
2. Los resultados de la liquidación de nómina alimentan la generación de los desprendibles PDF.
3. Los valores configurados en la parametrización SMMLV se aplican en el siguiente período de liquidación.

## APIs principales
### Nómina
- `POST /api/nomina/calcular/`
  - Body: `{ "periodo_inicio": "YYYY-MM-DD", "periodo_fin": "YYYY-MM-DD" }`
  - Response: Resultados de nómina por empleado.

### Desprendibles PDF
- `GET /api/desprendibles/generar/`
  - Query: `empleado_id` y `periodo` (formato YYYY-MM)
  - Response: Archivo PDF descargable.

### Parametrización SMMLV
- `GET /api/parametros/`: Lista todos los parámetros.
- `POST /api/parametros/`: Crea o actualiza un parámetro.
  - Body: `{ "clave": "SMMLV", "valor": "1300606.00" }`

## Detalles de implementación

### Motor de nómina (`empleados_nomina`)
- Cálculo de salario base.
- Horas extra diurnas: 25% sobre el valor hora base.
- Horas extra nocturnas: 75% sobre el valor hora base.
- Recargos dominicales y festivos según CST colombiano.
- Deducciones: salud (4%), pensión (4%), ARL (valor parametrizado).
- Integración con modelo `Asistencia` para obtener horas trabajadas.
- Modelo `LiquidacionNomina` para almacenar resultados por período y empleado.

### Generación de desprendibles PDF (`empleados_desprendibles`)
- Uso de biblioteca como ReportLab o WeasyPrint para generar PDF.
- Template con datos del empleado, devengados, deducciones y neto.
- Envío de email masivo utilizando el backend de correo de Django.
- Registro en auditoría de envíos exitosos/fallidos.
- Modelo `Desprendible` para rastrear estado (generado, enviado, fallido).

### Parametrización SMMLV (`empleados_parametros`)
- Extiende el modelo existente `ParametroSistema`.
- Interfaz de administración simple (lista de clave-valor con descripción).
- Historial de cambios integrado con la tabla `Auditoria`.
- Validación de tipos (numérico, fecha, etc.) según la clave.
- Endpoints protegidos por rol `ADMIN_SISTEMA`.

## Manejo de errores
- Validación rigurosa de datos de entrada (fechas, existencia de empleado activo).
- Captura de excepciones en envío de emails con reintentos y logging.
- Respuestas HTTP apropiadas (400 para errores de cliente, 500 para errores de servidor).
- Logging de operaciones críticas y fallos para depuración.

## Testing
- **Unitarios**: Lógica de cálculo de nómina (casos de borde), validación de parámetros.
- **Integración**: Flujos completos (asistencia → nómina → PDF), actualización de parámetros afecta liquidación.
- **Facturas**: Verificación de generación de PDF correcta, contenido esperado, simulación de envío de email.

## Dependencias
- ReportLab o WeasyPrint para generación de PDF.
- Django core (ya existente).
- Ninguna dependencia externa crítica adicional.

## Consideraciones de seguridad
- Las APIs están protegidas por autenticación y permisos de rol.
- Los parámetros de SMMLV solo pueden ser modificados por `ADMIN_SISTEMA`.
- Los datos de nómina son sensibles; acceso restringido a roles autorizados.
- Los archivos PDF generados se sirven de forma segura (almacenamiento temporal o streaming).

## Próximos pasos
Tras la aprobación de este diseño, se creará el plan de implementación usando la skill `writing-plans`.