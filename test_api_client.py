import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User

user = User.objects.first()
client = APIClient()
client.force_authenticate(user=user)
response = client.post('/api/nomina/generar/', {'mes': '7', 'ano': 2026}, format='json')

print("STATUS:", response.status_code)
print("DATA:", response.data)

from backend.empleados.models import Nomina
Nomina.objects.all().delete()
