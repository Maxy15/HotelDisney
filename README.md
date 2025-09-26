# Sorteo San Valentín en Hotel Disney 🏰

Aplicación web sencilla creada con Django para el *backend*, Nuxt para el *frontend* y una pequeña base de datos local en un archivo SQLite llamado ```db.sqlite3```. Esta permite a los usuarios registrarse en un concurso para ganar 2 noches con todo pagado en el Hotel Disney (pequeña licencia creativa). Para confirmar su participación, los concursantes deben validarse y crear una contraseña a través del link que llega a sus correos. Por otro lado, el usuario administrador puede ver todos los participantes, lanzar el sorteo para decidir al ganador y eliminar todos los usuarios para volver a crear otro sorteo. Hay una demostración disponible en el video `Demo.mov` guardado en la carpeta `docs`.

## Guía de instalación manual

### Backend
```sh
cd backend

# Instalar Python
brew install python@3.11

# Entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Base de datos
python manage.py makemigrations api --name initial
python manage.py migrate

# Seed del usuario admin
python manage.py shell -c "from api.seeds import create_admin_user; create_admin_user()"

# Verificar
python manage.py dbshell
sqlite> .tables
sqlite> select * from users;
sqlite> .quit

# Servidor (terminal 1)
python manage.py runserver 8000

# Redis (terminal 2)
# La instalación de Redis puede variar según SO
source venv/bin/activate
brew services start redis
redis-server

# Celery (terminal 3)
source venv/bin/activate
pkill -9 -f 'celery worker'
python -c "from decouple import config; import os; [os.environ.setdefault(k, config(k, default='')) for k in ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'EMAIL_BACKEND']]" && celery -A cts_backend worker --loglevel=info

# Puedes borrar la base de datos y ejecutar nuevamente si es necesario
rm db.sqlite3  
rm -rf api/migrations/__pycache__

# Para finalizar el entorno virtual
deactivate
```

### Frontend
```sh
cd frontend

# Instalar NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

# Instalar Node 18
nvm install 18
nvm use 18
nvm alias default 18
node -v
npm -v

# Instalar dependencias
npm install

# Preparar Nuxt
npx nuxt prepare

# Levantar frontend
npm run dev
```
## API endpoints

### Públicos
| Método | Endpoint                          | Descripción         |
| ------ | --------------------------------- | ------------------- |
| `GET`  | `/api/health/`                    | Health check        |
| `POST` | `/api/users/register/`            | Registro de usuario |
| `GET`  | `/api/users/token/?token={token}` | Validar token       |
| `POST` | `/api/users/set-password/`        | Crear contraseña    |

### Admin (requiere Bearer token)
| Método   | Endpoint                | Descripción     |
| -------- | ----------------------- | --------------- |
| `POST`   | `/api/admin/login/`     | Login admin     |
| `GET`    | `/api/admin/all-users/` | Listar usuarios |
| `GET`    | `/api/admin/winner/`    | Realizar sorteo |
| `DELETE` | `/api/admin/clear-db/`  | Limpiar BD      |

## Documentación API

### Health check
```http
GET /api/health/
```

**Response**
```json
{
  "code"    : 200,
  "message" : "Healthy a las 25/09/2025 22:17:23 hrs",
  "success" : true
}
```

---

### Registro de Usuario
```http
POST /api/users/register/
```

**Body**
```json
{
  "nombre"        : "Ricardo Bascuñan",
  "email"         : "richi.bascunan@transelec.org",
  "telefono"      : "+56911112222",
  "nombre_pareja" : "Dua Lipa"
}
```

**Response**
```json
{
  "code"    : 201,
  "message" : "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.",
  "success" : true
}
```

---

### Validar token
```http
GET /api/users/token/?token=ce6ddf29-879b-478a-b47c-9a4c80528238
```

**Response**
```json
{
  "code"    : 200,
  "message" : "Token válido",
  "user"    : {
    "nombre" : "Test User 25",
    "email"  : "test25@ejemplo.com"
  },
  "success" : true
}
```

---

### Crear contraseña
```http
POST /api/users/set-password/
```

**Body**
```json
{
  "token"            : "ce6ddf29-879b-478a-b47c-9a4c80528238",
  "password"         : "123456",
  "confirm_password" : "123456"
}
```

**Response**
```json
{
  "code"     : 200,
  "message"  : "Tu cuenta ha sido activada. Ya estás participando en el sorteo.",
  "user": {
    "nombre" : "Test User 25",
    "email"  : "test25@ejemplo.com",
    "status" : "CONFIRMADO"
  },
  "success"  : true
}
```

---

### Login admin
```http
POST /api/admin/login/
```

**Body**
```json
{
  "email"    : "admin@cts.cl",
  "password" : "adminglobal"
}
```

**Response**
```json
{
  "code"    : 200,
  "message" : "Login exitoso",
  "token"   : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "user"    : {
    "nombre" : "Administrador CTS",
    "email"  : "admin@cts.cl"
  },
  "success" : true
}
```

---

### Listar usuarios
```http
GET /api/admin/all-users/
Authorization: Bearer {token}
```
**Response**
```json
{
  "code"    : 200,
  "users"   : [
    {
      "id_usuario"      : 2,
      "nombre"          : "Test User",
      "email"           : "test@ejemplo.com",
      "telefono"        : "+56912345678",
      "nombre_pareja"   : "Test Partner",
      "status"          : "CONFIRMADO",
      "can_participate" : true
    }
  ],
  "total"   : 1,
  "success" : true
}
```

---

### Realizar sorteo
```http
GET /api/admin/winner/
Authorization: Bearer {token}
```
**Response**
```json
{
  "code"                : 200,
  "message"             : "Ganador seleccionado exitosamente",
  "winner"              : {
    "id_usuario"       : 27,
    "nombre"           : "Test User 25",
    "email"            : "test25@ejemplo.com",
    "telefono"         : "+56912345678",
    "nombre_pareja"    : "Test Partner",
    "last_time_winner" : "2025-09-26T00:20:00.306136-03:00"
  },
  "total_participants"  : 1,
  "success"             : true
}
```

---

### Limpiar base de datos
```http
DELETE /api/admin/clear-db/
Authorization: Bearer {token}
```
**Response**
```json
{
  "code"          : 200,
  "message"       : "Base de datos limpiada. 2 usuarios eliminados",
  "deleted_count" : 2,
  "success"       : true
}
```

---

## Tecnologías

### Backend
- **Python 3.11**
- **Django 4.2.7** - Framework web principal
- **Django Rest Framework 3.14.0** - API REST
- **Celery 5.3.4** - Tareas asíncronas (envío de emails)
- **Redis 5.0.1** - Broker para Celery
- **SQLite** - Base de datos local ligera
- **bcrypt** - Encriptación de contraseñas
- **PyJWT** - Tokens de verificación

### Frontend
- **Nuxt 3.8.0** - Framework Vue.js sencillo
- **Vue 3.3.8** - Framework JavaScript reactivo
- **Tailwind CSS 3.x** - Framework de estilos
- **TypeScript** - Tipado estático
- **Axios** - Cliente HTTP

### DevOps
- **Docker** - Containerización
- **Redis** - Cache y message broker

## Requisitos
- **Docker** si se desea utilizar los contenedores de cada parte de la aplicación
- **Git** para clonar el repositorio
  - Puertos disponibles: `3000` (frontend), `8000` (backend) y `6379` (Redis)

## Ejemplos de variables de entorno

### Backend
```sh
# Django
DEBUG=1
SECRET_KEY=django-insecure-dev-key-please-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend

# Database (En DEV SQLite no necesita más configs)
# DB_NAME=db.sqlite3

# Redis (para Celery)
# REDIS_URL=redis://redis:6379/0 # Para Docker
REDIS_URL=redis://127.0.0.1:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=max.y.orias@gmail.com

# Contraseña de aplicación (configurable desde Google)
EMAIL_HOST_PASSWORD=thmvqplljcgppqww
DEFAULT_FROM_EMAIL=noreply@ctsturismo.cl

# JWT
JWT_SECRET_KEY=jwt-dev-secret-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=600

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend
```sh
API_BASE_URL=http://localhost:8000/api
FRONTEND_URL=http://localhost:3000
NUXT_ENV=development
```

## Administrador
Las credenciales del usuario administrador son creados por el archivo `seeds.py` ubicado en la carpeta `/backend/api/`. Estan son las siguientes:
- **Email**: `admin@cts.cl`
- **Contraseña**: `adminglobal`

## Principales características
- Contraseñas encriptadas con bycript
- Uso de JWT para autentificar la sesión de los administradores
- Uso de token UUID con expiración de 10 minutos para verificación de usuarios
- CORS configurado
- Logs de información, advertencia y error
- Diseño UI ambientado con paleta de colores que hace referencia a San Valentín
- Archivos `Dockerfile` para el backend y el frontend

## Posibles mejoras futuras
- Migrar base de datos SQLite a Cloud SQL e implementar Memcache oara Redis
- Implementar API Rate Limiting con Load Balancer para manejar alta demanda
- Orquestación de contenedores con Cloud Run o Kubernetes
- Uso de certificados SSL/TLS para comunicación segura
- Mejoras iconografía UI (por temas de tiempo ahora son emojis)

> Desarrollado con mucha cafeína por Max Yáñez ☕
