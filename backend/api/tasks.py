from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_verification_email(self, email, nombre, token):
  """Send verification email to user"""
  try:
    verification_url = f"http://localhost:3000/verify?token={token}"
    subject          = 'Verificación de cuenta - Sorteo San Valentín en Hotel Disney 💕'
    message          = f"""
    ¡Hola {nombre}! 💕
    
    ¡Gracias por registrarte en nuestro sorteo especial de San Valentín! ✨
    
    Para completar tu registro y participar en el sorteo para ganar 
    2 noches mágicas en el Hotel Disney con tu pareja, necesitas 
    verificar tu correo electrónico.
    
    Haz clic en el siguiente enlace para crear tu contraseña:
    {verification_url}
    
    ⚠️ Este enlace expira en 10 minutos por seguridad.
    
    ¡Que la magia de Disney los acompañe!
    Equipo CTS Turismo
    
    ---
    Este es un correo automático, por favor no respondas a este mensaje.
    """
    
    email_msg = EmailMessage(
      subject=subject,
      body=message,
      from_email=settings.DEFAULT_FROM_EMAIL,
      to=[email]
    )
    email_msg.send(fail_silently=False)
    
    logger.info(f"Email de verificación enviado con éxito a {email}")
    return f"Email de verifcación enviado con éxito a {email}"
      
  except Exception as exc:
    logger.error(f"Error intentando enviar email de verificación a {email}: {str(exc)}")
    raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_winner_email(self, user_id, email, nombre, nombre_pareja):
  """Enviar al ganador una notificación por email"""
  try:
    subject = '🎉 ¡FELICIDADES! Ganaste el sorteo de San Valentín Disney'
    message = f"""    
    ¡Felicidades a {nombre} y a {nombre_pareja}! 💕
    
    ¡Han ganado 2 noches con todo pagado en el hotel de sus sueños! 🏰
    
    🎁 Tu premio incluye:
    • 2 noches de hospedaje en Hotel Disney
    • Desayuno incluido
    • Acceso completo a las instalaciones
    • Una experiencia mágica e inolvidable
    
    Nuestro equipo se comunicará contigo en las próximas 24 horas 
    para coordinar todos los detalles de tu premio.
    
    ¡Prepárense para vivir la magia de Disney juntos! 💖
    
    Con mucha emoción,
    Equipo CTS Turismo ✨
        
    ---
    Este es un correo automático, por favor no respondas a este mensaje.
    Para consultas, contacta a nuestro equipo de atención al cliente.
    """
    
    email_msg = EmailMessage(
      subject=subject,
      body=message,
      from_email=settings.DEFAULT_FROM_EMAIL,
      to=[email]
    )
    email_msg.send(fail_silently=False)
    
    logger.info(f"Email de notificación al ganador enviado exitosamente a {email}")
    return f"Email de notificación al ganador enviado exitosamente a {email}"
      
  except Exception as exc:
    logger.error(f"Error enviando email de notificación al ganador {email}: {str(exc)}")
    raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
