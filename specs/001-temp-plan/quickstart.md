# Quick Start Guide: Sprint 4 - Reportes y Exportación

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL (for production) or SQLite (for development)
- Git

## Backend Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd SOFTVAR
git checkout 001-temp-plan
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the backend directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3  # For development
# For PostgreSQL: DATABASE_URL=postgres://user:password@localhost:5432/sofvar
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Load initial data (if needed)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Run development server
```bash
python manage.py runserver
```

Backend API will be available at: http://localhost:8000

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables
Create a `.env` file in the frontend directory:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Sistema de Asistencia y Nómina
```

### 4. Run development server
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## Testing

### Backend Tests
```bash
# From backend directory
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
# From frontend directory
npm run test
```

### Run all tests
```bash
# From project root
./run-tests.sh  # If script exists
```

## Key Features to Test

### 1. Dashboard de Reportes (Gerente)
- Login as gerente user
- Navigate to Dashboard section
- Verify charts load with sample data
- Test filtering by year and employee

### 2. Reportes Filtrables (Gerente)
- Login as gerente user
- Navigate to Reportes Filtrables section
- Apply filters (date range, employee type)
- Verify results display correctly
- Test export to Excel, CSV, PDF

### 3. Exportación ACH para Bancos (Contador)
- Login as contador user
- Navigate to Nomina > Exportación ACH
- Select liquidación y banco
- Generate and download ACH file
- Verify file format matches bank specifications

### 4. Exportación a Excel (Contador)
- Login as contador user
- Navigate to Nomina > Exportación a Excel
- Select date range and options
- Generate and download Excel file
- Verify multiple sheets and correct data

### 5. Auditoría de Cambios (Administrador del Sistema)
- Login as admin user
- Navigate to Auditoría section
- Apply filters (date, action, table)
- Verify audit log entries display correctly
- Test statistics view

## Project Structure Reference

### Backend (Django)
```
backend/
├── empleados/              # Main app
│   ├── migrations/
│   ├── models.py          # Contains data models
│   ├── views.py           # API views
│   ├── serializers.py     # Data serialization
│   ├── urls.py            # URL routing
│   ├── admin.py           # Django admin config
│   ├── apps.py
│   ├── utils.py
│   ├── nomina_engine.py   # Payroll calculation logic
│   └── tests/
├── usuarios/               # User management (if separate)
├── settings.py
├── urls.py
└── manage.py
```

### Frontend (Vue.js)
```
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── layout/
│   │   ├── forms/
│   │   └── widgets/
│   ├── router/
│   ├── stores/           # Pinia stores
│   ├── views/
│   │   ├── empleados/
│   │   ├── nomina/
│   │   ├── reportes/
│   │   └── auditoria/
│   ├── services/
│   │   ├── api.js        # API service layer
│   │   └── auth.js
│   ├── App.vue
│   └── main.js
└── tests/
```

## Common Commands

### Backend
```bash
# Run server
python manage.py runserver

# Run tests
pytest

# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run unit tests
npm run test

# Run end-to-end tests
npm run test:e2e

# Lint code
npm run lint

# Fix lint errors
npm run lint -- --fix
```

## Deployment Preparation

### 1. Production Settings
Create `backend/settings_production.py`:
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
DATABASE_URL = os.environ.get('DATABASE_URL')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=production-secret-key
DATABASE_URL=postgres://user:password@host:5432/dbname
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 3. Build and Deploy
```bash
# Backend
pip install -r requirements.txt
python manage.py migrate --settings=backend.settings_production
python manage.py collectstatic --settings=backend.settings_production

# Frontend
npm run build
# Deploy dist/ folder to web server
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check DATABASE_URL in .env
   - Ensure PostgreSQL/SQLite is running
   - Run migrations: `python manage.py migrate`

2. **CORS issues**
   - Verify django-cors-headers is installed
   - Check CORS_ALLOWED_ORIGINS in settings.py

3. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings

4. **API authentication failing**
   - Verify JWT token is being sent correctly
   - Check token expiration time
   - Ensure user has correct permissions

5. **Excel/PDF generation errors**
   - Check pandas/openpyxl/reportlab versions
   - Verify file permissions for temporary files
   - Check memory limits for large datasets

## Contact and Support

For questions or issues during implementation:
- Refer to the data-model.md for database schema details
- Consult api-contracts.md for endpoint specifications
- Check CLAUDE.md for UI/UX guidelines and color standards
- Review existing code in backend/empleados/ for patterns and conventions

## Next Steps

After verifying basic functionality:
1. Implement role-based access controls for all new endpoints
2. Add comprehensive unit and integration tests
3. Performance test with realistic data volumes
4. Prepare user documentation and training materials
5. Plan deployment to staging environment