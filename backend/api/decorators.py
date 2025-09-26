from .models import User
from django.conf import settings
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
import jwt
import logging

logger = logging.getLogger(__name__)

def admin_required(view_func):
  """
  Decorador para validar token JWT y verificar rol de admin
  """
  @wraps(view_func)
  def wrapped_view(request, *args, **kwargs):
    # Obtener token del header Authorization
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
      return Response(
        {
          'code'    : 401,
          'message' : 'Token de autenticación requerido',
          'success' : False
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    
    # Verificar formato "Bearer <token>"
    try:
      token_type, token = auth_header.split()
      if token_type.lower() != 'bearer':
        raise ValueError('Formato de token inválido')
    except ValueError:
      return Response(
        {
          'code'    : 401,
          'message' : 'Formato de token inválido. Use: Bearer <token>',
          'success' : False
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    
    # Decodificar y validar token
    try:
      payload = jwt.decode(
        token, 
        settings.JWT_SECRET_KEY, 
        algorithms=[settings.JWT_ALGORITHM]
      )
      
      # Verificar que el usuario existe
      user = User.objects.get(id_usuario=payload['user_id'])
      
      # Verificar que tiene rol ADMIN
      if payload.get('role') != 'ADMIN' or not user.roles.filter(rol='ADMIN').exists():
        return Response(
          {
            'code'    : 403,
            'message' : 'No tienes permisos de administrador',
            'success' : False
          },
          status=status.HTTP_403_FORBIDDEN
        )
      
      # Agregar usuario al request para uso posterior
      request.user = user
        
    except jwt.ExpiredSignatureError:
      return Response(
        {
          'code': 401,
          'message': 'Token expirado',
          'success': False
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    except jwt.InvalidTokenError:
      return Response(
        {
          'code'    : 401,
          'message' : 'Token inválido',
          'success' : False
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    except User.DoesNotExist:
      return Response(
        {
          'code'    : 401,
          'message' : 'Usuario no encontrado',
          'success' : False
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    except Exception as e:
      logger.error(f"Error validando token - {str(e)}")
      return Response(
        {
          'code'    : 500,
          'message' : 'Error al validar token',
          'success' : False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    
    # Si todo está bien, ejecutar la vista
    return view_func(request, *args, **kwargs)
  
  return wrapped_view