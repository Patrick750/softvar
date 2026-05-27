# Research Findings: Sprint 4 - Reportes y Exportación

## Decision: Technical Stack Confirmation
- **Decision**: Confirm use of Django 4.2, Vue.js 3, SQLite/PostgreSQL
- **Rationale**: Existing codebase already uses these technologies; maintains consistency and leverages existing team expertise
- **Alternatives considered**: 
  - Node.js/Express backend (would require rewrite)
  - React frontend (would require learning new framework)
  - MongoDB (would require significant schema changes)

## Decision: Report Generation Libraries
- **Decision**: Use reportlab for PDF generation, pandas/openpyxl for Excel export
- **Rationale**: These are mature, well-documented libraries that integrate well with Django
- **Alternatives considered**:
  - WeasyPrint for PDF (steeper learning curve)
  - XlsxWriter for Excel (similar functionality to openpyxl)
  - Django built-in serialization (limited formatting capabilities)

## Decision: ACH File Format
- **Decision**: Generate delimited .txt files with configurable format per bank
- **Rationale**: Matches requirement for bank-specific ACH formats; simple to implement and configure
- **Alternatives considered**:
  - Fixed-width format (more complex to configure)
  - XML format (overkill for simple bank transfers)
  - JSON (not standard for bank ACH files)

## Decision: Audit Query Implementation
- **Decision**: Create read-only API endpoints for audit consultation
- **Rationale**: Matches existing pattern in codebase; ensures proper authentication and authorization
- **Alternatives considered**:
  - Direct database access (security risk)
  - File-based logs (harder to query and filter)
  - Third-party audit tools (adds external dependency)

## Decision: Charting Library for Dashboard
- **Decision**: Use Chart.js or Vue wrapper for charts in dashboard
- **Rationale**: Popular, well-maintained, good integration with Vue.js
- **Alternatives considered**:
  - D3.js (more powerful but steeper learning curve)
  - ApexCharts (good alternative but less community support)
  - Highcharts (licensing costs)

## Decision: Export Configuration Management
- **Decision**: Store bank ACH format configurations in ParametroSistema model
- **Rationale**: Leverages existing parametrization system; allows runtime changes without code deploy
- **Alternatives considered**:
  - Hard-coded formats (not flexible)
  - Separate configuration files (requires file system access)
  - Database table for each bank format (over-engineered)