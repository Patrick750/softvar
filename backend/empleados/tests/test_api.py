from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from empleados.models import Empleado

class EmpleadoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a superuser for authentication
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        # Authenticate
        self.client.force_authenticate(user=self.admin_user)

    def test_get_empleados_list(self):
        url = reverse('empleado-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect empty list initially
        self.assertEqual(len(response.data), 0)

    def test_create_empleado(self):
        url = reverse('empleado-list')
        data = {
            'cedula': '1234567890',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'email': 'juan.perez@example.com',
            'cargo': 'Desarrollador Senior',
            'tipo_contrato': 'TERMINO_FIJO',
            'salario_base': '3000000.00',
            'fecha_ingreso': '2026-01-15',
            'eps': 'Sura',
            'afp': 'Porvenir',
            'arl': 'Positiva',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cedula'], '1234567890')

    def test_generar_nomina(self):
        # Create an employee first
        Empleado.objects.create(
            user=self.admin_user,
            cedula='123456',
            nombres='Prueba',
            apellidos='Nomina',
            email='test@example.com',
            cargo='Desarrollador Senior',
            tipo_contrato='TERMINO_FIJO',
            salario_base='2400000.00', # 10,000 per hour
            fecha_ingreso='2026-01-01',
            eps='Sura',
            afp='Porvenir',
            arl='Positiva',
            activo=True
        )

        url = reverse('nomina-generar')
        data = {
            'mes': 6,
            'ano': 2026,
            'novedades': {}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_devengados']), 2400000.00)
        
        # Check that it prevents duplicate generation
        response_dup = self.client.post(url, data, format='json')
        self.assertEqual(response_dup.status_code, status.HTTP_400_BAD_REQUEST)
