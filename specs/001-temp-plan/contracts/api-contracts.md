# API Contracts: Sprint 4 - Reportes y Exportación

## Backend API Endpoints

### Dashboard de Reportes (Gerente)

#### GET /api/reportes/dashboard/
Obtiene datos para el dashboard de reportes comparativos por mes.

**Query Parameters:**
- `year`: Integer (required) - Año para el reporte
- `mes_inicio`: Integer (1-12) - Mes de inicio (default: enero)
- `mes_fin`: Integer (1-12) - Mes de fin (default: diciembre)
- `empleado_id`: Integer (optional) - Filtrar por empleado específico

**Response:**
```json
{
  "meses": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
  "datasets": {
    "dias_trabajados": {
      "label": "Días Trabajados",
      "data": [22, 20, 22, 21, 23, 20, 22, 21, 22, 20, 22, 21],
      "backgroundColor": "rgba(56, 138, 221, 0.5)",
      "borderColor": "rgba(56, 138, 221, 1)"
    },
    "ausencias": {
      "label": "Ausencias",
      "data": [2, 1, 0, 1, 0, 2, 1, 0, 1, 2, 1, 0],
      "backgroundColor": "rgba(163, 45, 45, 0.5)",
      "borderColor": "rgba(163, 45, 45, 1)"
    },
    "horas_extras": {
      "label": "Horas Extras",
      "data": [10, 8, 12, 6, 15, 9, 11, 7, 10, 8, 12, 9],
      "backgroundColor": "rgba(99, 153, 34, 0.5)",
      "borderColor": "rgba(99, 153, 34, 1)"
    },
    "costo_total": {
      "label": "Costo Total por Empleado ($)",
      "data": [1200, 1100, 1250, 1180, 1300, 1150, 1220, 1190, 1230, 1120, 1260, 1200],
      "backgroundColor": "rgba(24, 95, 165, 0.5)",
      "borderColor": "rgba(24, 95, 165, 1)"
    }
  },
  "totales": {
    "dias_trabajados": 255,
    "ausencias": 12,
    "horas_extras": 118,
    "costo_promedio": 1210
  }
}
```

#### GET /api/reportes/dashboard/resumen/
Obtiene resumen ejecutivo de métricas clave.

**Response:**
```json
{
  "periodo": "Enero 2026",
  "total_empleados": 45,
  "asistencias_registradas": 842,
  "horas_extras_totales": 118,
  "ausentismo_porcentaje": 2.5,
  "costo_nomina_total": 54450,
  "tendencia": {
    "asistencias": "+2.3%",
    "horas_extras": "-1.2%",
    "ausentismo": "-0.8%",
    "costo": "+3.1%"
  }
}
```

### Reportes Filtrables (Gerente)

#### GET /api/reportes/filtrables/
Obtiene datos filtrados para reportes.

**Query Parameters:**
- `tipo`: String (required) - Tipo de reporte: asistencia, nomina, incidencias
- `fecha_inicio`: Date (required, format: YYYY-MM-DD)
- `fecha_fin`: Date (required, format: YYYY-MM-DD)
- `empleado_id`: Integer (optional)
- `formato`: String (optional) - json, excel, csv (default: json)
- `pagina`: Integer (optional, default: 1)
- `por_pagina`: Integer (optional, default: 50)

**Response (JSON format):**
```json
{
  "count": 125,
  "next": "http://example.com/api/reportes/filtrables/?pagina=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "empleado": {
        "id": 1,
        "nombres": "Juan",
        "apellidos": "Pérez",
        "cedula": "1234567890",
        "cargo": "Desarrollador Senior"
      },
      "fecha": "2026-01-15",
      "tipo": "asistencia",
      "detalle": {
        "entrada": "08:00",
        "salida": "17:00",
        "horas_trabajadas": 8,
        "horas_extra": 0,
        "estado": "EXITO"
      }
    }
  ],
  "filtros_aplicados": {
    "tipo": "asistencia",
    "fecha_inicio": "2026-01-01",
    "fecha_fin": "2026-01-31",
    "empleado_id": null
  }
}
```

#### POST /api/reportes/filtrables/exportar/
Exporta resultados filtrados en el formato especificado.

**Body:**
```json
{
  "tipo": "asistencia",
  "fecha_inicio": "2026-01-01",
  "fecha_fin": "2026-01-31",
  "empleado_id": null,
  "formato": "excel", // json, excel, csv
  "incluir_detalles": true
}
```

**Response (for excel/csv):** Archivo para descarga
**Response (for json):** Mismo formato que GET anterior

### Exportación ACH para Bancos (Contador)

#### GET /api/nomina/configuraciones-ach/
Lista configuraciones ACH disponibles por banco.

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "banco": "Bancolombia",
      "formato_cuenta": "00123456789",
      "formato_valor": "00000000012345",
      "formato_nombre": "APELLIDOS NOMBRE          ",
      "delimiter": ",",
      "longitud_linea": 0,
      "activo": true
    },
    {
      "id": 2,
      "banco": "Davivienda",
      "formato_cuenta": "123456789",
      "formato_valor": "0000000012345",
      "formato_nombre": "NOMBRE APELLIDO         ",
      "delimiter": ";",
      "longitud_linea": 30,
      "activo": true
    }
  ]
}
```

#### POST /api/nomina/generar-ach/
Genera archivo ACH para transferencia bancaria.

**Body:**
```json
{
  "liquidacion_id": 1,
  "banco_config_id": 1,
  "fecha_pago": "2026-01-31"
}
```

**Response:** Archivo .txt para descarga con formato:
```
00123456789,00000000012345001500000,JUAN PEREZ          ,
00123456790,00000000009876000800000,MARIA GONZALEZ      ,
...
```

#### GET /api/nomina/descargar-ach/{id}/
Descarga un archivo ACH previamente generado.

**Response:** Archivo .txt para descarga

### Exportación a Excel (Contador)

#### GET /api/nomina/exportar-excel/
Exporta liquidaciones de nómina a formato Excel.

**Query Parameters:**
- `periodo_inicio`: Date (required)
- `periodo_fin`: Date (required)
- `empleado_ids`: String (optional, comma-separated list of IDs)
- `incluir_detalles`: Boolean (default: true)
- `formato`: String (optional) - xlsx, xls (default: xlsx)

**Response:** Archivo .xlsx para descarga con hojas:
- Resumen por empleado
- Detalle de devengados
- Detalle de deducciones
- Resumen financiero

#### POST /api/nomina/programar-exportacion/
Programa exportación automática de Excel.

**Body:**
```json
{
  "nombre": "Reporte Mensual Enero 2026",
  "periodo_inicio": "2026-01-01",
  "periodo_fin": "2026-01-31",
  "frecuencia": "MENSUAL",
  "dia_mes": 5,
  "hora": "08:00:00",
  "activo": true,
  "emails": ["contabilidad@empresa.com", "gerencia@empresa.com"]
}
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Reporte Mensual Enero 2026",
  "proximo_envio": "2026-02-05T08:00:00Z",
  "activo": true
}
```

### Auditoría de Cambios (Consulta) (Administrador del Sistema)

#### GET /api/auditoria/
Obtiene registros de auditoría con filtros.

**Query Parameters:**
- `tabla_afectada`: String (optional)
- `accion`: String (optional)
- `fecha_inicio`: Date (optional)
- `fecha_fin`: Date (optional)
- `usuario_id`: Integer (optional)
- `pagina`: Integer (optional, default: 1)
- `por_pagina`: Integer (optional, default: 100)
- `ordenar`: String (optional, default: -fecha_hora)

**Response:**
```json
{
  "count": 245,
  "next": "http://example.com/api/auditoria/?pagina=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "usuario": {
        "id": 1,
        "username": "admin",
        "first_name": "Administrador",
        "last_name": "Sistema"
      },
      "fecha_hora": "2026-01-15T10:30:00Z",
      "tabla_afectada": "asistencias",
      "registro_id": 125,
      "accion": "INTENTO_FALLIDO",
      "valor_anterior": null,
      "valor_nuevo": "{\"verificacion_facial_score\": 0.65, \"liveness_score\": 0.8}",
      "ip_address": "192.168.1.100"
    }
  ]
}
```

#### GET /api/auditoria/estadisticas/
Obtiene estadísticas de auditoría.

**Response:**
```json
{
  "total_registros": 245,
  "por_accion": {
    "CREAR": 45,
    "MODIFICAR": 32,
    "ELIMINAR": 8,
    "INICIO_SESION": 89,
    "INTENTO_FALLIDO": 61,
    "APROBAR_MANUAL": 10
  },
  "por_tabla": {
    "asistencias": 120,
    "empleados": 35,
    "liquidaciones_nomina": 25,
    "usuarios": 15,
    "parametros_sistema": 10
  },
  "intentos_fallidos_por_dia": [
    {"fecha": "2026-01-10", "count": 2},
    {"fecha": "2026-01-11", "count": 5},
    {"fecha": "2026-01-12", "count": 3}
  ]
}
```

### Configuración de Reportes y Filtros Guardados

#### GET /api/reportes/filtros-guarded/
Lista filtros guardados por usuario.

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "nombre": "Asistencia Enero - Todos",
      "tipo_reporte": "asistencia",
      "fecha_inicio": "2026-01-01",
      "fecha_fin": "2026-01-31",
      "empleados": [], // vacío = todos
      "incluir_horas_extra": true,
      "formato_exportacion": "excel",
      "creado_en": "2026-01-15T09:00:00Z",
      "actualizado_en": "2026-01-15T09:00:00Z"
    }
  ]
}
```

#### POST /api/reportes/filtros-guarded/
Guarda un nuevo filtro de reporte.

**Body:**
```json
{
  "nombre": "Nomina Febrero - Desarrolladores",
  "tipo_reporte": "nomina",
  "fecha_inicio": "2026-02-01",
  "fecha_fin": "2026-02-28",
  "empleados": [1, 2, 3, 4, 5], // IDs de empleados developers
  "incluir_horas_extra": false,
  "formato_exportacion": "excel"
}
```

**Response:** Objeto creado con ID y timestamps

#### PUT /api/reportes/filtros-guarded/{id}/
Actualiza un filtro guardado existente.

#### DELETE /api/reportes/filtros-guarded/{id}/
Elimina un filtro guardado.

## Authentication and Authorization

All endpoints require authentication via JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Role-based Access Control:

- **Gerente**: Puede acceder a endpoints de dashboard y reportes filtrables
- **Contador**: Puede acceder a endpoints de nómina, exportación ACH y Excel
- **Administrador del Sistema**: Puede acceder a endpoints de auditoría y configuración del sistema
- **Administrador de RRHH**: Acceso limitado a reportes básicos de empleados
- **Empleado**: Solo acceso a su propio historial (endpoints específicos no listados aquí)

## Error Responses

Standard error response format:
```json
{
  "error": "Error description",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "Specific error details"
  }
}
```

Common error codes:
- `VALIDATION_ERROR`: Error de validación en los datos de entrada
- `PERMISSION_DENIED`: Usuario no tiene permisos para acceder al recurso
- `RESOURCE_NOT_FOUND`: Recurso solicitado no existe
- `INTERNAL_ERROR`: Error interno del servidor
- `INVALID_TOKEN`: Token de autenticación inválido o expirado

## Rate Limiting

API endpoints are subject to rate limiting:
- Authenticated users: 1000 requests/hour
- Anonymous users: 100 requests/hour
- Burst limit: 50 requests/minute

## Data Format Standards

### Dates:
- Input/Output: ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- Fecha sola: YYYY-MM-DD
- Fecha y hora: YYYY-MM-DDTHH:MM:SSZ

### Numbers:
- Decimals: Siempre usar punto como separador decimal
- Enteros: Sin formato, solo dígitos
- Monedas: En la unidad base (pesos colombianos) sin formato

### Text:
- Codificación: UTF-8
- Trim: Los strings se guardan trimmeados en base de datos
- Longitud máxima: Según definición en modelo de datos

## Versioning

API version is included in URL path: `/api/v1/`
Future versions will maintain backward compatibility where possible.
Deprecation notices will be provided 30 days in advance for breaking changes.