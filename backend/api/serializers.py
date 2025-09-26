from rest_framework import serializers
from .models import User, Role
import re
import logging

logger = logging.getLogger(__name__)

class UserRegistrationSerializer(serializers.ModelSerializer):
  """Serializer de registro de usuario"""
  
  class Meta:
    model  = User
    fields = ['nombre', 'email', 'telefono', 'nombre_pareja']
  
  def validate_email(self, value):
    """Validar unicidad y formato de email"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
      raise serializers.ValidationError("Formato de email inválido")
    
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("Este email ya está registrado")
    
    return value.lower()
  
  def validate_telefono(self, value):
    """
    Validar teléfonos chilenos móviles con el formato: '+569 12345678'
    Reglas:
      - Debe ser celular (empieza con 9) y tener 8 dígitos después del 9.
      - Acepta prefijos +56, 56, 09, espacios y símbolos.
    """
    # Dejar solo dígitos
    digits = re.sub(r'\D', '', value)

    # Quitar prefijo país '56' si viene
    if digits.startswith('56'):
      digits = digits[2:]

    # Quitar cero inicial (caso '09')
    if digits.startswith('0'):
      digits = digits[1:]

    # Debe ser móvil: comenzar con '9' y tener 9 dígitos en total (9 + 8)
    if not digits.startswith('9'):
      raise serializers.ValidationError("Debe ser un celular chileno (empieza con +569)")
    local = digits[1:]

    if len(local) != 8 or not local.isdigit():
      raise serializers.ValidationError("Formato inválido - se esperan 8 dígitos después del 9")

    return f"+569{local}"
  
  def validate_nombre(self, value):
    """Validar nombre"""
    if len(value.strip()) < 2:
      raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
    return value.strip().title()
  
  def validate_nombre_pareja(self, value):
    """Validar nombre de pareja"""
    if len(value.strip()) < 2:
      raise serializers.ValidationError("El nombre de la pareja debe tener al menos 2 caracteres")
    return value.strip().title()
  
  def create(self, validated_data):
    """Crear nuevo usuario y generar token de verificación"""
    user = User.objects.create(**validated_data)
    user.generate_verification_token()
    user.save()
    
    Role.objects.create(id_usuario=user, rol='CONCURSANTE')
    logger.info(f"Nuevo usuario registrado: {user.email}")
    return user
  
class TokenValidationSerializer(serializers.Serializer):
  """Serializer para validar el token"""
  token = serializers.CharField(required=True)
  
  def validate_token(self, value):
    """Validar si el token existe y es válido"""
    try:
      user = User.objects.get(verification_token=value)
      if not user.is_token_valid():
          raise serializers.ValidationError("El token ha expirado")
      return value
    except User.DoesNotExist:
      raise serializers.ValidationError("Token inválido")

class UserVerificationSerializer(serializers.Serializer):
    """Serializer para verificación del usuario y creación de contraseña"""
    token            = serializers.CharField(required=True)
    password         = serializers.CharField(min_length=6, required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
      """Validar contraseña y que el token sea válido"""
      if data['password'] != data['confirm_password']:
        raise serializers.ValidationError("Las contraseñas no coinciden")
      
      try:
        user = User.objects.get(verification_token=data['token'])
        if not user.is_token_valid():
          raise serializers.ValidationError("El token ha expirado. Solicita un nuevo enlace de verificación")
        data['user'] = user
      except User.DoesNotExist:
        raise serializers.ValidationError("Token de verificación inválido")
      
      return data
    
    def save(self):
      """Guardar contraseña y actualizar status"""
      user                     = self.validated_data['user']
      user.set_password(self.validated_data['password'])
      user.status              = 'CONFIRMADO'
      user.verification_token  = None
      user.token_created_at    = None
      user.save()
      
      logger.info(f"Usuario CONFIRMADO: {user.email}")
      return user


class AdminLoginSerializer(serializers.Serializer):
  """Serializer para el login del admin"""
  email    = serializers.EmailField(required=True)
  password = serializers.CharField(required=True)
  
  def validate(self, data):
    """Validar credenciales con mensajes específicos"""
    try:
      user = User.objects.get(email=data['email'])
      
      # Verificar si el usuario tiene rol ADMIN
      if not user.roles.filter(rol='ADMIN').exists():
        raise serializers.ValidationError({
          "email": "Este usuario no tiene permisos de administrador"
        })
      
      # Verificar contraseña
      if not user.check_password(data['password']):
        raise serializers.ValidationError({
          "password": "Contraseña incorrecta"
        })
      
      data['user'] = user
        
    except User.DoesNotExist:
      raise serializers.ValidationError({
        "email": "No existe un usuario con este correo"
      })
    
    return data


class UserListSerializer(serializers.ModelSerializer):
  """Serializer para listar los usuarios"""
  roles           = serializers.StringRelatedField(many=True, read_only=True)
  can_participate = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = [
      'id_usuario', 
      'nombre', 
      'email',
      'telefono', 
      'nombre_pareja', 
      'status', 
      'inserted_at', 
      'updated_at', 
      'last_time_winner', 
      'roles', 
      'can_participate'
    ]
  
  def get_can_participate(self, obj):
    return obj.can_participate()


class WinnerSerializer(serializers.ModelSerializer):
  """Serializer para mostrar al usuario ganador"""
  
  class Meta:
    model  = User
    fields = [
      'id_usuario', 
      'nombre', 
      'email', 
      'telefono',
      'nombre_pareja', 
      'last_time_winner'
    ]
