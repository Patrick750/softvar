from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import Empleado, Nomina, DetalleNomina

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def _auto_set_foto_registrada(self, validated_data):
        """Automatically set foto_facial_registrada based on foto_facial presence."""
        if 'foto_facial' in validated_data:
            validated_data['foto_facial_registrada'] = bool(validated_data['foto_facial'])
        return validated_data

    def create(self, validated_data):
        validated_data = self._auto_set_foto_registrada(validated_data)
        email = validated_data.get('email')
        cedula = validated_data.get('cedula')
        nombres = validated_data.get('nombres', '')
        apellidos = validated_data.get('apellidos', '')
        
        # User details
        username = cedula
        temp_password = get_random_string(length=10)
        
        first_name = nombres.split(' ')[0] if nombres else ""
        last_name = apellidos.split(' ')[0] if apellidos else ""
        
        # Create django user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Assign to EMPLEADO group
        group, _ = Group.objects.get_or_create(name='EMPLEADO')
        user.groups.add(group)
        
        # Print credentials in terminal for debugging
        print("\n" + "="*50)
        print(f"NUEVAS CREDENCIALES CREADAS PARA: {nombres} {apellidos}")
        print(f"Usuario: {username}")
        print(f"Contraseña temporal: {temp_password}")
        print("="*50 + "\n")

        # Send welcome email
        subject = 'Bienvenido a SoftVar - Credenciales de Acceso'
        message = f"""Hola {nombres} {apellidos},
        
Te damos la bienvenida al Sistema de Control de Asistencia y Nómina SoftVar.
Se ha creado tu cuenta con las siguientes credenciales temporales:

Usuario (Cédula): {username}
Contraseña temporal: {temp_password}

Por favor, inicia sesión en http://localhost:5173/login y cambia tu contraseña en tu Portal Personal.

Atentamente,
El Equipo de Recursos Humanos
"""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error al enviar correo de credenciales: {e}")
            
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._auto_set_foto_registrada(validated_data)
        email = validated_data.get('email')
        if email and instance.user and instance.user.email != email:
            instance.user.email = email
            instance.user.save()
            
        cedula = validated_data.get('cedula')
        if cedula and instance.user and instance.user.username != cedula:
            instance.user.username = cedula
        return super().update(instance, validated_data)

class DetalleNominaSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField(source='empleado.nombres', read_only=True)
    apellidos = serializers.CharField(source='empleado.apellidos', read_only=True)
    cedula = serializers.CharField(source='empleado.cedula', read_only=True)

    class Meta:
        model = DetalleNomina
        fields = '__all__'

class NominaSerializer(serializers.ModelSerializer):
    detalles = DetalleNominaSerializer(many=True, read_only=True)

    class Meta:
        model = Nomina
        fields = '__all__'