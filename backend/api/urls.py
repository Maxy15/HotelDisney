from django.urls import path
from . import views

urlpatterns = [
  # Health check
  path('health/', views.health_check, name='health_check'),
  
  # Endpoints del usuario
  path('users/register/', views.register_user, name='register_user'),
  path('users/token/', views.validate_token, name='validate_token'),
  path('users/set-password/', views.set_password, name='set_password'),
  
  # Endpoints del admin
  path('admin/login/', views.admin_login, name='admin_login'),
  path('admin/all-users/', views.get_all_users, name='get_all_users'),
  path('admin/winner/', views.draw_winner, name='draw_winner'),
  path('admin/clear-db/', views.clear_database, name='clear_database'),
]