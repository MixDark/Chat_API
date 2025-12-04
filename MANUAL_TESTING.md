# Guía de pruebas manuales - Chat API

Esta guía muestra cómo probar manualmente todos los endpoints de la API usando Insomnia.

## Iniciar el servidor

Primero, asegúrate de que el servidor esté corriendo:

```bash
python run.py
```

Deberías ver:
```
 * Running on http://0.0.0.0:7000
 * Debug mode: on
```

## Usar Insomnia

### Instalación

1. Descargar Insomnia: https://insomnia.rest/download
2. Instalar y abrir Insomnia
3. Crear una nueva colección: Click en "+" → "Request Collection" → Nombrar "Chat API Tests"

### Configuración de requests

#### 1. Health Check 

- Click en "New Request" (o presiona `Ctrl+N`)
- Name: `Health Check`
- Method: `GET`
- URL: `http://localhost:7000/api/health`
- Click en `Send`

Respuesta esperada:
```json
{
	"message": "API is running",
	"status": "healthy"
}
```

---

## Autenticación con API Keys

#### 2. Crear API Key

- New Request
- Name: `Create API Key`
- Method: `POST`
- URL: `http://localhost:7000/api/auth/keys`
- Body → Seleccionar `JSON`:

```json
{
  "name": "Mi API Key de Prueba"
}
```

Respuesta esperada:
```json
{
	"data": {
		"api_key": "80d180da92e1247244636914a198102746f715f5b1f95b0c156a081edc70cfa9",
		"key_info": {
			"created_at": "2025-12-04T16:46:53.797149Z",
			"id": 1,
			"is_active": true,
			"last_used_at": null,
			"name": "Mi API Key de Prueba"
		}
	},
	"message": "Guarda esta API Key de forma segura. No se mostrará nuevamente.",
	"status": "success"
}
```

IMPORTANTE: Copia el valor de "api_key" para usarlo en las siguientes pruebas.

---

#### 3. Listar API Keys

- New Request
- Name: `List API Keys`
- Method: `GET`
- URL: `http://localhost:7000/api/auth/keys`
- Click en `Send`

Respuesta esperada:
```json
{
	"data": [
		{
			"created_at": "2025-12-04T16:46:53.797149Z",
			"id": 1,
			"is_active": true,
			"last_used_at": null,
			"name": "Mi API Key de Prueba"
		}
	],
	"status": "success"
}
```

---

#### 4. Revocar API Key

- New Request
- Name: `Revoke API Key`
- Method: `DELETE`
- URL: `http://localhost:7000/api/auth/keys/1` (reemplaza 1 con el ID de tu API Key)
- Click en `Send`

Respuesta esperada:
```json
{
	"message": "API Key revocada exitosamente",
	"status": "success"
}
```

Si intentas revocar una API Key que no existe:
```json
{
	"error": {
		"code": "NOT_FOUND",
		"message": "API Key no encontrada"
	},
	"status": "error"
}
```

---

## Pruebas de Mensajes

NOTA: La autenticación es opcional. Puedes agregar el header X-API-Key o no.

Para agregar autenticación en Insomnia:
- Ve a la pestaña "Header"
- Agrega: `X-API-Key` con el valor de tu API Key

#### 5. Crear mensaje del sistema 

- New Request
- Name: `Create System Message`
- Method: `POST`
- URL: `http://localhost:7000/api/messages`
- Header (opcional): `X-API-Key: tu-api-key-aqui`
- Body → Seleccionar `JSON`:

```json
{
  "message_id": "msg-001",
  "session_id": "session-test-123",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2025-12-04T17:00:00Z",
  "sender": "system"
}
```

---

#### 6. Crear mensaje del usuario 

- New Request
- Name: `Create User Message`
- Method: `POST`
- URL: `http://localhost:7000/api/messages`
- Body → `JSON`:

```json
{
  "message_id": "msg-002",
  "session_id": "session-test-123",
  "content": "Necesito ayuda con mi cuenta",
  "timestamp": "2025-12-04T17:01:00Z",
  "sender": "user"
}
```

---

#### 7. Obtener todos los mensajes 

- New Request
- Name: `Get All Messages`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123`

---

#### 8. Obtener mensajes con paginación 

- New Request
- Name: `Get Messages with Pagination`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123?limit=5&offset=0`

---

#### 9. Filtrar por remitente (usuario) 

- New Request
- Name: `Filter Messages by User`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123?sender=user`

---

#### 10. Filtrar por remitente (sistema) 

- New Request
- Name: `Filter Messages by System`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123?sender=system`

---

## Búsqueda de Mensajes

#### 11. Buscar por contenido

- New Request
- Name: `Search Messages by Content`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123/search?q=ayuda`

Busca mensajes que contengan la palabra "ayuda"

---

#### 12. Buscar por rango de fechas

- New Request
- Name: `Search Messages by Date Range`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123/search?start_date=2025-12-04T00:00:00Z&end_date=2025-12-04T23:59:59Z`

---

#### 13. Búsqueda combinada

- New Request
- Name: `Search Combined Filters`
- Method: `GET`
- URL: `http://localhost:7000/api/messages/session-test-123/search?q=cuenta&sender=user&limit=10`

---

## Probar Rate Limiting

#### 14. Exceder límite de requests

- Usa cualquier endpoint de mensajes
- Envía más de 20 requests en menos de 1 minuto
- Deberías recibir error 429:

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Demasiadas solicitudes. Por favor intenta más tarde."
  }
}
```

---

## Probar Filtrado de Contenido

#### 15. Mensaje con palabras filtradas

- New Request
- Name: `Content Filtering`
- Method: `POST`
- URL: `http://localhost:7000/api/messages`
- Body → `JSON`:

```json
{
  "message_id": "msg-003",
  "session_id": "session-test-123",
  "content": "Este es un mensaje con spam y scam",
  "timestamp": "2025-12-04T17:05:00Z",
  "sender": "user"
}
```

El contenido filtrado será: "Este es un mensaje con **** y ****"

---

## Probar Validación de Errores

#### 16. Campos faltantes

- New Request
- Name: `Missing Fields`
- Method: `POST`
- URL: `http://localhost:7000/api/messages`
- Body → `JSON`:

```json
{
  "message_id": "msg-004",
  "content": "Mensaje sin session_id"
}
```

Error esperado: MISSING_FIELDS

---

#### 17. Sender inválido

```json
{
  "message_id": "msg-005",
  "session_id": "session-test-123",
  "content": "Mensaje de prueba",
  "timestamp": "2025-12-04T17:00:00Z",
  "sender": "admin"
}
```

Error esperado: INVALID_SENDER

---

#### 18. Timestamp inválido

```json
{
  "message_id": "msg-006",
  "session_id": "session-test-123",
  "content": "Mensaje de prueba",
  "timestamp": "fecha-invalida",
  "sender": "user"
}
```

Error esperado: INVALID_TIMESTAMP

---

#### 19. Message ID duplicado

Envía el mismo mensaje dos veces con el mismo message_id.

Error esperado: DUPLICATE_MESSAGE_ID

---

## Probar WebSocket (Cliente HTML)

1. Abre el archivo `examples/websocket_client.html` en tu navegador
2. Ingresa un Session ID (ej: session-test-123)
3. Click en "Unirse a sesión"
4. En Insomnia, crea un nuevo mensaje con el mismo session_id
5. Deberías ver el mensaje aparecer en tiempo real en el cliente HTML

---

## Solución de problemas

### El servidor no responde
- Verifica que `python run.py` esté corriendo
- Asegúrate de usar el puerto correcto (7000)
- Revisa que no haya errores en la consola del servidor

### Error "Connection refused"
- El servidor no está corriendo
- Ejecuta `python run.py` primero

### Error 404 en todos los endpoints
- Verifica la URL: debe incluir `/api/` en la ruta
- Ejemplo correcto: `http://localhost:7000/api/messages`

### Errores de JSON en Insomnia
- Asegúrate de seleccionar "JSON" en el tipo de Body
- Verifica que el JSON esté bien formado (sin comas extras, comillas correctas)
- Usa el validador integrado de Insomnia

### Error 401 Unauthorized
- Si el endpoint requiere autenticación, agrega el header X-API-Key
- Verifica que la API Key sea válida y esté activa

### WebSocket no conecta
- Asegúrate de que el servidor esté corriendo con socketio.run
- Verifica que no haya firewall bloqueando el puerto 7000
- Revisa la consola del navegador para ver errores de conexión
