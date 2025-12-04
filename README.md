# Chat API

API RESTful para procesamiento de mensajes de chat construida con Flask, que valida, procesa y almacena mensajes de chat, proporcionando capacidades de recuperación con filtrado y paginación.

## Características

### Funcionalidades Core
- **API RESTful** con endpoints para crear y recuperar mensajes
- **Validación completa** de mensajes con manejo robusto de errores
- **Pipeline de procesamiento** con filtrado de contenido inapropiado
- **Generación automática de metadatos** (conteo de palabras, caracteres, timestamp de procesamiento)
- **Paginación y filtrado** en la recuperación de mensajes
- **Arquitectura limpia** con separación de responsabilidades (utils, services, repositories, tests)
- **Pruebas completas** con cobertura del 80%+
- **Manejo de errores** con códigos HTTP apropiados y mensajes descriptivos

### Funcionalidades Avanzadas
- **Autenticación con API Keys** - Sistema de autenticación simple y seguro
- **WebSocket en tiempo real** - Actualizaciones instantáneas de mensajes
- **Búsqueda avanzada** - Búsqueda por contenido, fechas y remitente
- **Rate Limiting** - Protección contra abuso con límites configurables
- **Soporte Docker** - Containerización completa con Docker y Docker Compose
- **Infraestructura como código** - Deployment automatizado en AWS con Terraform

## Requisitos

- Python 3.10+
- Flask
- SQLite (incluido con Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd chat_api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
python run.py
```

El servidor estará disponible en `http://localhost:7000`

### Verificar que la API está funcionando

```bash
curl http://localhost:7000/api/health
```

## Documentación de la API

### 1. Crear mensaje

**Endpoint:** `POST /api/messages`

**Descripción:** Crea y procesa un nuevo mensaje de chat.

**Request Body:**
```json
{
  "message_id": "msg-001",
  "session_id": "session-test-123",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2025-12-03T17:00:00Z",
  "sender": "system"
}
```

**Campos requeridos:**
- `message_id` (string): Identificador único del mensaje
- `session_id` (string): Identificador de sesión
- `content` (string): Contenido del mensaje
- `timestamp` (string): Marca de tiempo en formato ISO 8601
- `sender` (string): Remitente del mensaje ("user" o "system")

**Response exitosa (201 Created):**
```json
{
	"data": {
		"content": "Hola, ¿cómo puedo ayudarte hoy?",
		"message_id": "msg-001",
		"metadata": {
			"character_count": 31,
			"processed_at": "2025-12-03T21:59:47Z",
			"word_count": 5
		},
		"sender": "system",
		"session_id": "session-test-123",
		"timestamp": "2025-12-03T17:00:00Z"
	},
	"status": "success"
}
```

### 2. Recuperar mensajes

**Endpoint:** `GET /api/messages/<session_id>`

**Descripción:** Recupera todos los mensajes de una sesión con soporte para paginación y filtrado.

**Parámetros de consulta (opcionales):**
- `limit` (int): Número máximo de mensajes a retornar (default: 10, max: 100)
- `offset` (int): Número de mensajes a omitir (default: 0)
- `sender` (string): Filtrar por remitente ("user" o "system")

**Response exitosa (200 OK):**
```json
{
	"data": [
		{
			"content": "Hola, ¿cómo puedo ayudarte hoy?",
			"message_id": "msg-001",
			"metadata": {
				"character_count": 31,
				"processed_at": "2025-12-03T21:59:47Z",
				"word_count": 5
			},
			"sender": "system",
			"session_id": "session-test-123",
			"timestamp": "2025-12-03T17:00:00Z"
		},
		{
			"content": "Necesito ayuda con mi cuenta",
			"message_id": "msg-002",
			"metadata": {
				"character_count": 28,
				"processed_at": "2025-12-03T22:01:02Z",
				"word_count": 5
			},
			"sender": "user",
			"session_id": "session-test-123",
			"timestamp": "2025-12-03T17:01:00Z"
		},
		{
			"content": "Este es un mensaje con **** y ****",
			"message_id": "msg-003",
			"metadata": {
				"character_count": 34,
				"processed_at": "2025-12-03T22:02:57Z",
				"word_count": 8
			},
			"sender": "user",
			"session_id": "session-test-123",
			"timestamp": "2025-12-03T17:05:00Z"
		}
	],
	"pagination": {
		"limit": 10,
		"offset": 0,
		"total": 3
	},
	"status": "success"
}
```

### 3. Health Check

**Endpoint:** `GET /api/health`

**Descripción:** Verifica que la API está funcionando.

**Response (200 OK):**
```json
{
	"message": "API is running",
	"status": "healthy"
}
```

### 4. Autenticación - Crear API Key

**Endpoint:** `POST /api/auth/keys`

**Descripción:** Crea una nueva API Key para autenticación.

**Request Body:**
```json
{
  "name": "Mi Aplicación"
}
```

**Response exitosa (201 Created):**
```json
{
  "status": "success",
  "data": {
    "api_key": "a1b2c3d4e5f6...",
    "key_info": {
      "id": 1,
      "name": "Mi Aplicación",
      "created_at": "2025-12-04T15:00:00Z",
      "is_active": true
    }
  },
  "message": "Guarda esta API Key de forma segura. No se mostrará nuevamente."
}
```

**Uso de API Key:**
Agrega el header `X-API-Key` a tus requests:
```bash
curl -H "X-API-Key: tu-api-key-aqui" http://localhost:7000/api/messages
```

### 5. Listar API Keys

**Endpoint:** `GET /api/auth/keys`

**Descripción:** Lista todas las API Keys creadas.

**Response exitosa (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Mi Aplicación",
      "created_at": "2025-12-04T15:00:00Z",
      "last_used_at": "2025-12-04T16:30:00Z",
      "is_active": true
    },
    {
      "id": 2,
      "name": "App de Prueba",
      "created_at": "2025-12-04T15:30:00Z",
      "last_used_at": null,
      "is_active": true
    }
  ]
}
```

### 6. Revocar API Key

**Endpoint:** `DELETE /api/auth/keys/<key_id>`

**Descripción:** Revoca una API Key existente.

**Response exitosa (200 OK):**
```json
{
  "status": "success",
  "message": "API Key revocada exitosamente"
}
```

**Error si no existe (404 Not Found):**
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "API Key no encontrada"
  }
}
```

### 7. Búsqueda de Mensajes

**Endpoint:** `GET /api/messages/<session_id>/search`

**Descripción:** Busca mensajes con múltiples filtros.

**Parámetros de consulta:**
- `q` (string): Texto a buscar en el contenido
- `start_date` (string): Fecha de inicio (ISO 8601)
- `end_date` (string): Fecha de fin (ISO 8601)
- `sender` (string): Filtrar por remitente
- `limit` (int): Número máximo de resultados
- `offset` (int): Número de resultados a omitir

**Ejemplo:**
```bash
curl "http://localhost:7000/api/messages/session-123/search?q=ayuda&sender=user"
```

### 8. WebSocket - Tiempo Real

**Conexión WebSocket:** `ws://localhost:7000`

**Eventos disponibles:**

- `connect` - Cliente conectado
- `join` - Unirse a room de sesión
  ```javascript
  socket.emit('join', { session_id: 'session-123' });
  ```
- `new_message` - Recibir nuevo mensaje
  ```javascript
  socket.on('new_message', (message) => {
    console.log('Nuevo mensaje:', message);
  });
  ```

**Cliente de ejemplo:** Ver `examples/websocket_client.html`


## Manejo de errores

La API retorna respuestas de error estructuradas:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Descripción del error",
    "details": {}
  }
}
```

### Códigos de error comunes

| Código HTTP | Error Code | Descripción |
|-------------|-----------|-------------|
| 400 | `INVALID_FORMAT` | El cuerpo de la solicitud no es un JSON válido |
| 400 | `MISSING_FIELDS` | Faltan campos requeridos |
| 400 | `INVALID_TYPE` | Un campo tiene un tipo incorrecto |
| 400 | `INVALID_TIMESTAMP` | El timestamp no está en formato ISO 8601 |
| 400 | `INVALID_SENDER` | El sender debe ser "user" o "system" |
| 400 | `EMPTY_CONTENT` | El contenido del mensaje está vacío |
| 400 | `DUPLICATE_MESSAGE_ID` | Ya existe un mensaje con ese ID |
| 401 | `MISSING_API_KEY` | Falta el header X-API-Key |
| 401 | `INVALID_API_KEY` | API Key inválida o revocada |
| 404 | `NOT_FOUND` | Recurso no encontrado |
| 405 | `METHOD_NOT_ALLOWED` | Método HTTP no permitido |
| 429 | `RATE_LIMIT_EXCEEDED` | Demasiadas solicitudes |
| 500 | `INTERNAL_SERVER_ERROR` | Error interno del servidor |

## Pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar pruebas con cobertura

```bash
pytest --cov=app --cov-report=html --cov-report=term
```

El reporte HTML se generará en `htmlcov/index.html`

### Ejecutar pruebas específicas

```bash
# Solo pruebas unitarias
pytest tests/test_services.py

# Solo pruebas de integración
pytest tests/test_endpoints.py
```

## Estructura del proyecto

```
chat_api/
├── app/
│   ├── __init__.py                  # Factory de la aplicación Flask
│   ├── models.py                    # Modelos de base de datos (Message, APIKey)
│   ├── routes.py                    # Endpoints de la API
│   ├── websocket_handlers.py        # Handlers de WebSocket
│   ├── services/
│   │   ├── __init__.py              # Inicialización del paquete
│   │   ├── validation_service.py    # Lógica de validación
│   │   ├── message_service.py       # Procesamiento de mensajes
│   │   ├── api_key_service.py       # Gestión de API Keys
│   │   └── search_service.py        # Servicio de búsqueda
│   ├── repositories/
│   │   ├── __init__.py              # Inicialización del paquete
│   │   └── message_repository.py    # Operaciones de base de datos
│   └── utils/
│       ├── __init__.py              # Inicialización del paquete
│       ├── validators.py            # Validadores y excepciones
│       ├── error_handlers.py        # Manejadores de errores
│       └── api_key_middleware.py    # Middleware de autenticación
├── tests/
│   ├── __init__.py                  # Inicialización del paquete
│   ├── conftest.py                  # Fixtures de pytest
│   ├── test_services.py             # Pruebas unitarias de servicios
│   ├── test_endpoints.py            # Pruebas de integración de endpoints
│   ├── test_auth.py                 # Pruebas de autenticación (API Keys)
│   ├── test_auth_endpoints.py       # Pruebas de endpoints de autenticación
│   ├── test_search.py               # Pruebas de búsqueda de mensajes
│   └── test_error_handlers.py       # Pruebas de manejadores de errores
├── terraform/
│   ├── main.tf                      # Configuración principal de Terraform
│   ├── variables.tf                 # Variables configurables
│   └── outputs.tf                   # Outputs de deployment
├── examples/
│   └── websocket_client.html        # Cliente WebSocket de ejemplo
├── htmlcov/                         # Reportes de cobertura HTML (generado)
├── .coverage                        # Datos de cobertura (generado)
├── .dockerignore                    # Archivos ignorados por Docker
├── .gitignore                       # Archivos ignorados por Git
├── Dockerfile                       # Configuración Docker multi-stage
├── docker-compose.yml               # Orquestación de contenedores
├── config.py                        # Configuración de entornos
├── run.py                           # Punto de entrada
├── requirements.txt                 # Dependencias Python
├── README.md                        # Documentación del proyecto
├── MANUAL_TESTING.md                # Guía de pruebas manuales
└── DEPLOYMENT.md                    # Guía de deployment en AWS
```

## Arquitectura

El proyecto sigue principios de **arquitectura limpia** con separación de responsabilidades:

- **Routes (Controladores)**: Manejan las peticiones HTTP y respuestas
- **Services (Servicios)**: Contienen la lógica de negocio
- **Repositories (Repositorios)**: Manejan las operaciones de base de datos
- **Utils (Utilidades)**: Funciones auxiliares y manejo de errores

### Flujo de procesamiento de mensajes

1. **Validación**: Se validan todos los campos requeridos y sus tipos
2. **Filtrado de contenido**: Se eliminan palabras inapropiadas
3. **Generación de metadatos**: Se calculan word_count, character_count y processed_at
4. **Almacenamiento**: Se guarda el mensaje en la base de datos
5. **Respuesta**: Se retorna el mensaje procesado con sus metadatos

## Configuración

El archivo `config.py` contiene configuraciones para diferentes entornos:

- **Development**: Base de datos SQLite local con debug activado
- **Testing**: Base de datos en memoria para pruebas
- **Production**: Configuración optimizada para producción

Para cambiar el entorno, establece la variable de entorno `FLASK_ENV`:

```bash
# Windows
set FLASK_ENV=production

# Linux/Mac
export FLASK_ENV=production
```

## Notas de implementación

### Filtrado de contenido

El sistema implementa un filtro simple de palabras inapropiadas. Las palabras filtradas incluyen:
- spam
- malware
- phishing
- scam

Las palabras filtradas se reemplazan con asteriscos (`****`).

### Base de datos

- Se utiliza SQLite
- La base de datos se crea automáticamente al iniciar la aplicación
- Para producción, se recomienda usar PostgreSQL o MySQL

### Validación de timestamps

Los timestamps deben estar en formato ISO 8601, ejemplos válidos:
- `2025-12-01T14:30:00Z`
- `2025-11-15T20:30:00+00:00`
- `2025-06-15T18:30:00.123Z`

### Rate Limiting

La API implementa límites de tasa para proteger contra abuso:

- **Global**: 100 requests por minuto
- **POST /api/messages**: 20 requests por minuto
- **GET /api/messages**: 60 requests por minuto
- **GET /api/messages/search**: 30 requests por minuto

Cuando se excede el límite, recibirás un error 429 con el mensaje correspondiente.

## Deployment con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
docker-compose up -d
```

La API estará disponible en `http://localhost:7000`

### Opción 2: Docker manual

```bash
# Construir imagen
docker build -t chat-api .

# Ejecutar contenedor
docker run -p 7000:7000 chat-api
```

### Opción 3: Deployment en AWS con Terraform

Ver documentación completa en [DEPLOYMENT.md](DEPLOYMENT.md)

Pasos básicos:

1. Construir y subir imagen a ECR
2. Ejecutar `terraform apply` en el directorio `terraform/`
3. Acceder a la API via DNS del ALB

La infraestructura incluye:
- VPC con subnets públicas
- Application Load Balancer
- ECS Fargate para containers
- CloudWatch Logs
- Security Groups configurados

## Recursos adicionales

- **Guía de pruebas manuales**: Ver [MANUAL_TESTING.md](MANUAL_TESTING.md)
- **Guía de deployment**: Ver [DEPLOYMENT.md](DEPLOYMENT.md)
- **Cliente WebSocket de ejemplo**: Ver `examples/websocket_client.html`
- **Configuración Terraform**: Ver directorio `terraform/`
