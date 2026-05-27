# Sprint 4 Plan: Reportes y Exportación

## Objetivo
Implementar módulos de reportes y exportación para gerente y contador, incluyendo:
- Dashboard de reportes
- Reportes filtrables
- Exportación ACH para bancos
- Exportación a Excel
- Consulta de auditoría de cambios

## Roles involucrados
- Gerente (color UI: #042C53 - Azul oscuro)
- Contador (color UI: #3B6D11 - Verde principal)
- Administrador del sistema (para auditoría)

## Módulos a desarrollar

### 1. Dashboard de reportes (Gerente)
- Gráficas de barras comparativas por mes:
  - Días trabajados
  - Ausencias
  - Horas extras
  - Costo total por empleado
- Fuente de datos: módulos de asistencia y nómina

### 2. Reportes filtrables (Gerente)
- Filtrar por rango de fechas y empleado
- Exportar resultados a Excel (.xlsx)
- Fuente de datos: módulos de asistencia y nómina

### 3. Exportación ACH para bancos (Contador)
- Generar archivo .txt delimitado con:
  - Cuenta bancaria
  - Valor a pagar
  - Nombre del empleado
- Formato configurable por entidad bancaria
- Fuente de datos: liquidación de nómina

### 4. Exportación a Excel (Contador)
- Generar archivo .xlsx con detalle completo del período liquidado
- Incluir: devengados, deducciones, neto, etc.
- Fuente de datos: liquidación de nómina

### 5. Auditoría de cambios (consulta) (Administrador del sistema)
- Consultar historial inmutable de modificaciones en asistencia:
  - Usuario
  - Fecha/hora
  - Valor anterior
  - Valor nuevo
- Solo lectura

## Tecnologías
- Backend: Django (Python)
- Frontend: Vue.js
- Base de datos: SQLite
- Colores semánticos según CLAUDE.md:
  - Éxito/Aprobado: #EAF3DE (fondo) / #3B6D11 (acento)
  - Alerta/Pendiente: #FAEEDA (fondo) / #854F0B (acento)
  - Error/Rechazado: #FCEBEB (fondo) / #A32D2D (acento)
  - Info/En proceso: #E6F1FB (fondo) / #185FA5 (acento)

## Estándares de calidad
- Código limpio, funciones pequeñas y con responsabilidad única
- Pruebas unitarias y de integración (cobertura >= 80% en críticos)
- Consistencia UI: usar palette y componentes definidos
- Rendimiento: API < 200ms p95, carga inicial < 2s en 3G

## Dependencias entre módulos
- Dashboard y reportes filtrables dependen de datos de asistencia y nómina
- Exportaciones dependen del módulo de liquidación de nómina
- Auditoría de cambios registra intentos fallidos de reconocimiento facial/GPS

## Checklist de Definition of Done
- [ ] Código implementado y revisado
- [ ] Pruebas unitarias pasando
- [ ] Pruebas de integración pasando
- [ ] Documentación actualizada
- [ ] Despliegue en staging verificado
- [ ] Cumple con guía de estilos y paleta de colores
- [ ] No introduce vulnerabilidades de seguridad