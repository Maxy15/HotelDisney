from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import User, Role
import logging

logger = logging.getLogger(__name__)

def create_admin_user():
  """Crea el usuario admin"""
  try:
    with transaction.atomic():
      if User.objects.filter(email='admin@cts.cl').exists():
        logger.info("Admin user already exists")
        return
      
      admin_user = User.objects.create(
        nombre='Administrador CTS',
        email='admin@cts.cl',
        telefono='+56912345678',
        nombre_pareja='Sistema',
        status='CONFIRMADO'
      )
      
      admin_user.set_password('adminglobal')
      admin_user.save()
      
      Role.objects.create(
        id_usuario=admin_user,
        rol='ADMIN'
      )
      
      logger.info(f"Usuario administrador creado correctamente: {admin_user.email}")
        
  except Exception as e:
    logger.error(f"Error creando el usuario administrador: {str(e)}")
    raise


class Command(BaseCommand):
  """Comando de Django para crear data inicial"""
  help = 'Crear data inicial'
  
  def handle(self, *args, **options):
    self.stdout.write(
      self.style.SUCCESS('Creando data inicial...')
    )
    
    create_admin_user()
    
    self.stdout.write(
      self.style.SUCCESS('Data inicial creada exitosamente!')
    )


if __name__ == '__main__':
  create_admin_user()