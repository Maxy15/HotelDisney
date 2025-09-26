from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import bcrypt
import uuid
import logging
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

class User(models.Model):
  STATUS_CHOICES = [
    ('REGISTRADO', 'Registrado'),
    ('CONFIRMADO', 'Confirmado'),
    ('GANADOR', 'Ganador'),
  ]
  
  id_usuario        = models.AutoField(primary_key=True)
  nombre            = models.CharField(max_length=255, verbose_name="Nombre completo")
  email             = models.EmailField(unique=True, verbose_name="Correo electrónico")
  telefono          = models.CharField(max_length=20, verbose_name="Teléfono")
  nombre_pareja     = models.CharField(max_length=255, verbose_name="Nombre de la pareja")
  password_hash     = models.CharField(max_length=255, blank=True, null=True)
  status            = models.CharField(
    max_length=20, 
    choices=STATUS_CHOICES, 
    default='REGISTRADO',
    verbose_name="Estado"
  )
  inserted_at       = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
  updated_at        = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
  last_time_winner  = models.DateTimeField(blank=True, null=True, verbose_name="Última vez ganador")
  
  # Token para verificar usuario
  verification_token = models.CharField(max_length=255, blank=True, null=True)
  token_created_at   = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    db_table            = 'users'
    verbose_name        = "Usuario"
    verbose_name_plural = "Usuarios"
    ordering            = ['-inserted_at']
  
  def __str__(self):
    return f"{self.nombre} ({self.email})"
  
  def set_password(self, raw_password):
    """Crear hash de la contraseña con bcrypt"""
    salt   = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
    self.password_hash = hashed.decode('utf-8')
    logger.info(f"Contraseña guardada para {self.email}")
  
  def check_password(self, raw_password):
    """Validar contraseña"""
    if not self.password_hash:
      return False
    return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))
  
  def generate_verification_token(self):
    """Crear token de verificación"""
    self.verification_token = str(uuid.uuid4())
    self.token_created_at   = timezone.now()
    logger.info(f"Token de verificación generado para {self.email}")
    return self.verification_token
  
  def is_token_valid(self):
    """Validar si el token del usuario es válido (10 minutos máximo)"""
    if not self.token_created_at:
      return False
    
    expiry_time = self.token_created_at + timedelta(minutes=10)
    return timezone.now() <= expiry_time
  
  def can_participate(self):
    """Validar si el usuario puede participar en el sorteo"""
    return self.status == 'CONFIRMADO' and self.password_hash is not None
  
  def save(self, *args, **kwargs):
    logger.info(f"Guardando usuario {self.email} con status {self.status}")
    super().save(*args, **kwargs)


class Role(models.Model):
  ROLE_CHOICES = [
    ('ADMIN', 'Administrador'),
    ('CONCURSANTE', 'Concursante'),
  ]
  
  id_usuario = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    related_name='roles',
    verbose_name="Usuario"
  )

  rol = models.CharField(
    max_length=20, 
    choices=ROLE_CHOICES,
    verbose_name="Rol"
  )
  
  class Meta:
    db_table            = 'roles'
    unique_together     = ['id_usuario', 'rol']
    verbose_name        = "Rol"
    verbose_name_plural = "Roles"
  
  def __str__(self):
    return f"{self.id_usuario.email} - ROL: {self.rol}"