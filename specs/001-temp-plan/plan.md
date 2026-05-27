# Implementation Plan: Sprint 4 - Reportes y Exportación

**Branch**: `001-temp-plan` | **Date**: 2026-05-27 | **Spec**: specs/001-temp-plan/spec.md

**Input**: Feature specification from `/specs/001-temp-plan/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implementar módulos de reportes y exportación para gerente y contador, incluyendo dashboard de reportes, reportes filtrables, exportación ACH para bancos, exportación a Excel y consulta de auditoría de cambios. El proyecto usa Django (Python) para backend y Vue.js para frontend con SQLite como base de datos.

## Technical Context

**Language/Version**: Python 3.11, Django 4.2, Vue.js 3

**Primary Dependencies**: Django, Django REST Framework, pandas, openpyxl, reportlab, vue, vuetify, axios

**Storage**: SQLite (desarrollo), PostgreSQL (producción)

**Testing**: pytest (backend), Jest/Vitest (frontend)

**Target Platform**: Web application (responsive)

**Project Type**: Web application (backend + frontend)

**Performance Goals**: API < 200ms p95, carga inicial < 2s en 3G

**Constraints**: Cumplir con guía de estilos y paleta de colores definida en CLAUDE.md, cobertura de pruebas >= 80% en módulos críticos

**Scale/Scope**: Sistema para PyMES con hasta 100 empleados, reportes mensuales

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution template, the following gates apply:

- **Library-First**: Every feature starts as a standalone library; must be self-contained, independently testable, documented; clear purpose required.
- **CLI Interface**: Every library exposes functionality via CLI; text in/out protocol: stdin/args → stdout, errors → stderr; support JSON + human-readable formats.
- **Test-First (NON-NEGOTIABLE)**: TDD mandatory: tests written → user approved → tests fail → then implement; red-green-refactor cycle strictly enforced.
- **Integration Testing**: Focus areas requiring integration tests: new library contract tests, contract changes, inter-service communication, shared schemas.
- **Observability**: Text I/O ensures debuggability; structured logging required.
- **Versioning & Breaking Changes**: Use MAJOR.MINOR.BUILD format.
- **Simplicity**: Start simple, YAGNI principles.

**Assessment**: This feature (Sprint 4 reportes y exportación) will be implemented as part of the existing Django web application, not as a standalone library. However, we will adhere to the spirit of the constitution by ensuring modules are modular, well-tested, and documented. We will write tests first (TDD) for new backend endpoints and frontend components. We will ensure API endpoints return JSON and are usable by the frontend. We will add structured logging for key operations. We will follow semantic versioning for any internal packages we create.

No violations identified that require justification at this stage.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── empleados/           # Django app
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── utils.py
│   ├── nomina_engine.py
│   └── tests/
├── usuarios/            # Django app for user management (if exists)
│   └── ...
├── settings.py
├── urls.py
├── wsgi.py
├── asgi.py
└── manage.py

frontend/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── layout/
│   │   ├── forms/
│   │   └── widgets/
│   ├── router/
│   ├── stores/
│   ├── views/
│   │   ├── empleados/
│   │   ├── nomina/
│   │   ├── reportes/
│   │   └── auditoria/
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── App.vue
│   └── main.js
└── tests/
    ├── unit/
    └── e2e/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: Selected Option 2: Web application. The backend consists of Django apps (empleados, usuarios, etc.) under the backend/ directory. The frontend is a Vue.js application under the frontend/ directory (to be created). Tests are split between backend unit/integration tests and frontend unit/e2e tests.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
