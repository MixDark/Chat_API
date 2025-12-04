variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Nombre del entorno (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "app_name" {
  description = "Nombre de la aplicación"
  type        = string
  default     = "chat-api"
}

variable "container_cpu" {
  description = "CPU para el contenedor ECS (256, 512, 1024, 2048, 4096)"
  type        = string
  default     = "256"
}

variable "container_memory" {
  description = "Memoria para el contenedor ECS en MB (512, 1024, 2048, etc.)"
  type        = string
  default     = "512"
}

variable "desired_count" {
  description = "Número de instancias del servicio ECS"
  type        = number
  default     = 2
}
