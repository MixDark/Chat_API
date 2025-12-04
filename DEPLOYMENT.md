# Deployment - Chat API

Guía completa para desplegar el Chat API en AWS usando Terraform.

## Requisitos previos

- AWS CLI configurado con credenciales
- Terraform >= 1.0 instalado
- Docker instalado
- Cuenta de AWS con permisos necesarios

## Paso 1: Construir y subir imagen Docker

### Construir imagen localmente

```bash
docker build -t chat-api:latest .
```

### Autenticarse en ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

### Crear repositorio ECR (si no existe)

```bash
aws ecr create-repository --repository-name chat-api --region us-east-1
```

### Etiquetar y subir imagen

```bash
docker tag chat-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/chat-api:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/chat-api:latest
```

## Paso 2: Desplegar infraestructura con Terraform

### Inicializar Terraform

```bash
cd terraform
terraform init
```

### Revisar plan de deployment

```bash
terraform plan
```

### Aplicar configuración

```bash
terraform apply
```

Confirma con `yes` cuando se solicite.

### Obtener URL de la API

```bash
terraform output alb_dns_name
```

La API estará disponible en: `http://<ALB_DNS_NAME>/api/health`

## Paso 3: Verificar deployment

### Health check

```bash
curl http://<ALB_DNS_NAME>/api/health
```

### Crear mensaje de prueba

```bash
curl -X POST http://<ALB_DNS_NAME>/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-001",
    "session_id": "session-test",
    "content": "Hola desde AWS",
    "timestamp": "2025-12-04T15:00:00Z",
    "sender": "user"
  }'
```

## Arquitectura desplegada

La infraestructura incluye:

- VPC con 2 subnets públicas
- Application Load Balancer (ALB)
- ECS Cluster con Fargate
- ECR Repository para imágenes Docker
- Security Groups configurados
- CloudWatch Logs

## Actualizar la aplicación

### 1. Construir nueva imagen

```bash
docker build -t chat-api:latest .
```

### 2. Subir a ECR

```bash
docker tag chat-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/chat-api:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/chat-api:latest
```

### 3. Forzar nuevo deployment en ECS

```bash
aws ecs update-service --cluster chat-api-cluster --service chat-api-service --force-new-deployment --region us-east-1
```

## Destruir infraestructura

Para eliminar todos los recursos creados:

```bash
cd terraform
terraform destroy
```

Confirma con `yes` cuando se solicite.

## Costos estimados

Costos aproximados mensuales en us-east-1:

- ECS Fargate (2 tasks, 0.25 vCPU, 0.5 GB): ~$15/mes
- Application Load Balancer: ~$16/mes
- Data Transfer: Variable según uso
- CloudWatch Logs: ~$1/mes

Total estimado: ~$32/mes + data transfer

## Solución de problemas

### Tasks no inician

Verificar logs en CloudWatch:

```bash
aws logs tail /ecs/chat-api --follow --region us-east-1
```

### ALB no responde

Verificar security groups y health checks en la consola de AWS.

### Imagen no se encuentra

Asegurarse de que la imagen fue subida correctamente a ECR:

```bash
aws ecr describe-images --repository-name chat-api --region us-east-1
```
