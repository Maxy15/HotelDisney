from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from zoneinfo import ZoneInfo
import random
import logging
import jwt
import traceback
from django.conf import settings

from .decorators import admin_required
from .models import User, Role
from .serializers import (
  UserRegistrationSerializer,
  UserVerificationSerializer,
  AdminLoginSerializer,
  UserListSerializer,
  WinnerSerializer,
  TokenValidationSerializer
)
from .tasks import send_verification_email, send_winner_email

logger = logging.getLogger(__name__)

# HEALTH CHECK
# /api/health/
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
  """Endpoint de Health Check"""
  now_cl = timezone.localtime(timezone.now(), ZoneInfo(settings.TIME_ZONE))
  return Response(
    {
      'code'    : 200,
      'message' : f"Healthy a las {now_cl.strftime('%d/%m/%Y %H:%M:%S')} hrs",
      'success' : True
    }, 
    status=status.HTTP_200_OK
  )

# USER ENDPOINTS
# /api/users/register/
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
  """Registrar un nuevo usuario y enviar un mail de verificación"""
  try:
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
      user = serializer.save()
  
      logger.info(f"Celery Broker URL: {settings.CELERY_BROKER_URL}")
      try:
        send_verification_email.delay(
          user.email,
          user.nombre,
          user.verification_token
        )

      except Exception as e:
        logger.error(f"Error al enviar correo: {type(e).__name__}: {str(e)}")
        logger.error(f"Traceback completo:\n{traceback.format_exc()}")
        raise
      
      logger.info(f"Usuario registrado correctamente - {user.email}")
      
      return Response(
        {
          'code'    : 201,
          'message' : '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.',
          'success' : True
        }, 
        status=status.HTTP_201_CREATED
      )
      
    logger.warning(f"Error registrando usuario - {serializer.errors}")
    return Response(
      {
        'code'    : 400,
        'message' : f"Error en el registro - {serializer.errors}",
        'success' : False
      }, 
      status=status.HTTP_400_BAD_REQUEST
    )
      
  except Exception as e:
    logger.error(f"Error inesperado registrando usuario - {str(e)}")
    return Response(
      {
        'code'    : 500,
        'message' : 'Error interno del servidor',
        'success' : False
      }, 
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# /api/users/token/?token=987445
@api_view(['GET'])
@permission_classes([AllowAny])
def validate_token(request):
    """Validar token de verificación"""
    try:
      token = request.GET.get('token')
      
      if not token:
        return Response(
          {
            'code'   : 400,
            'message': 'Token requerido',
            'success': False
          }, 
          status=status.HTTP_400_BAD_REQUEST
        )
      
      serializer = TokenValidationSerializer(data={'token': token})
      
      if serializer.is_valid():
        user = User.objects.get(verification_token=token)
        
        return Response(
          {
            'code'    : 200,
            'message' : 'Token válido',
            'user'    : {
              'nombre': user.nombre,
              'email' : user.email
            },
            'success' : True
          }, 
          status=status.HTTP_200_OK
        )
      
      return Response(
        {
          'code'    : 400,
          'message' : 'Token inválido o expirado',
          'errors'  : serializer.errors,
          'success' : False
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )
        
    except Exception as e:
      logger.error(f"Error inesperado validando token - {str(e)}")
      return Response(
        {
          'code'    : 500,
          'message' : 'Error interno del servidor',
          'success' : False
        }, 
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

# /api/users/set-password/
@api_view(['POST'])
@permission_classes([AllowAny])
def set_password(request):
  """Crear contraseña para el usuario con token válido"""
  try:
    serializer = UserVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
      with transaction.atomic():
        user = serializer.save()
        logger.info(f"Password set successfully for user: {user.email}")
        return Response(
          {
            'code'     : 200,
            'message'  : 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.',
            'user'     : {
                'nombre' : user.nombre,
                'email'  : user.email,
                'status' : user.status
            },
            'success'  : True
          }, 
          status=status.HTTP_200_OK
        )
    
    logger.warning(f"Error al establecer contraseña - {serializer.errors}")
    return Response(
      {
        'code'    : 400,
        'message' : 'Error al establecer contraseña',
        'errors'  : serializer.errors,
        'success' : False
      }, 
      status=status.HTTP_400_BAD_REQUEST
    )
      
  except Exception as e:
    logger.error(f"Error inesperado al intentar guardar contraseña - {str(e)}")
    return Response(
      {
        'code'    : 500,
        'message' : 'Error interno del servidor',
        'success' : False
      }, 
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# ADMIN ENDPOINTS
# /api/admin/login/
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
  """Login del admin"""
  try:
    serializer = AdminLoginSerializer(data=request.data)
    
    if serializer.is_valid():
      user = serializer.validated_data['user']
      
      # Generar JWT para la sesión
      payload = {
        'user_id' : user.id_usuario,
        'email'   : user.email,
        'role'    : 'ADMIN',
        'exp'     : timezone.now().timestamp() + (60 * 60 * 24)  # 24 hours
      }
      
      token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
      logger.info(f"Login de admin {user.email} exitoso")
      
      return Response(
        {
          'code'    : 200,
          'message' : 'Login exitoso',
          'token'   : token,
          'user'    : {
            'nombre' : user.nombre,
            'email'  : user.email
          },
          'success' : True
        }, 
        status=status.HTTP_200_OK
      )
    
    # Manejar errores específicos del serializador
    logger.warning(f"Error en login de admin - {serializer.errors}")
    
    # Extraer el mensaje específico del error
    error_message = 'Credenciales inválidas'
    if 'email' in serializer.errors:
      error_message = serializer.errors['email'][0]
    elif 'password' in serializer.errors:
      error_message = serializer.errors['password'][0]
    elif 'non_field_errors' in serializer.errors:
      error_message = serializer.errors['non_field_errors'][0]
    
    return Response(
      {
        'code'   : 401,
        'message': error_message,
        'errors' : serializer.errors,
        'success': False
      }, 
      status=status.HTTP_401_UNAUTHORIZED
    )
      
  except Exception as e:
    logger.error(f"Error inesperado en login de admin - {str(e)}")
    return Response(
      {
        'code'   : 500,
        'message': 'Error interno del servidor',
        'success': False
      }, 
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# /api/admin/all-users/
@api_view(['GET'])
@admin_required
def get_all_users(request):
  """Obtener todos los usuarios"""
  try:
    users = User.objects.filter(
      roles__rol='CONCURSANTE'
    ).select_related().prefetch_related('roles')
    
    status_filter = request.GET.get('status')
    search        = request.GET.get('search')
    
    if status_filter:
      users = users.filter(status=status_filter)
    
    if search:
      from django.db import models
      users = users.filter(
        models.Q(nombre__icontains=search) |
        models.Q(email__icontains=search) |
        models.Q(nombre_pareja__icontains=search)
      )
    
    serializer = UserListSerializer(users, many=True)
    logger.info(f"Usuarios obtenidos exitosamente por admin: {request.user.email}")    
    return Response(
      {
        'code'    : 200,
        'users'   : serializer.data,
        'total'   : len(serializer.data),
        'success' : True
      }, 
      status=status.HTTP_200_OK
    )
      
  except Exception as e:
    logger.error(f"Error inesperado al obtener usuarios - {str(e)}")
    return Response(
      {
        'code'    : 500,
        'message' : 'Error al obtener usuarios',
        'success' : False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# /api/admin/winner/
@api_view(['GET'])
@admin_required
def draw_winner(request):
  """Obtener un ganador de los participantes elegibles"""
  try:
    eligible_users = User.objects.filter(
      status='CONFIRMADO',
      password_hash__isnull=False,
      roles__rol='CONCURSANTE'
    )
    
    if not eligible_users.exists():
      logger.warning("No hay participantes elegibles para el sorteo")
      return Response(
        {
          'code'    : 400,
          'message' : 'No hay participantes elegibles para el sorteo',
          'success' : False
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )
    
    winner = random.choice(eligible_users)
    with transaction.atomic():
      winner.status           = 'GANADOR'
      winner.last_time_winner = timezone.now()
      winner.save()
      
      logger.info(f"Ganador seleccionado por {request.user.email}: {winner.email}")
      
      send_winner_email.delay(
        winner.id_usuario,
        winner.email,
        winner.nombre,
        winner.nombre_pareja
      )
      
      serializer = WinnerSerializer(winner)
      
      return Response(
        {
          'code'               : 200,
          'message'            : 'Ganador seleccionado exitosamente',
          'winner'             : serializer.data,
          'total_participants' : eligible_users.count(),
          'success'            : True
        }, 
        status=status.HTTP_200_OK
      )
      
  except Exception as e:
    logger.error(f"Error inesperado al realizar sorteo - {str(e)}")
    return Response(
      {
        'code'    : 500,
        'message' : 'Error al realizar el sorteo',
        'success' : False
      }, 
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# /api/admin/clear-db/
@api_view(['DELETE'])
@admin_required
def clear_database(request):
  """Limpiar todos los usuarios menos el admin"""
  try:
    with transaction.atomic():
      deleted_count = User.objects.filter(
        roles__rol='CONCURSANTE'
      ).delete()[0]
      
      logger.info(f"Base de datos limpiada por {request.user.email}")
      logger.info(f"{deleted_count} usuarios eliminados")
      
      return Response(
        {
          'code'          : 200,
          'message'       : f'Base de datos limpiada. {deleted_count} usuarios eliminados',
          'deleted_count' : deleted_count,
          'success'       : True
        }, 
        status=status.HTTP_200_OK
      )
      
  except Exception as e:
    logger.error(f"Error inesperado limpiando base de datos - {str(e)}")
    return Response(
      {
        'code'    : 500,
        'message' : 'Error al limpiar la base de datos',
        'success' : False
      }, 
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )