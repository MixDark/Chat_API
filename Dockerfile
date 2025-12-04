# Multi-stage build para optimizar tamaño de imagen

# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Copiar dependencias instaladas desde builder
COPY --from=builder /root/.local /root/.local

# Copiar código de la aplicación
COPY . .

# Asegurar que los scripts de Python usen las dependencias instaladas
ENV PATH=/root/.local/bin:$PATH

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exponer puerto
EXPOSE 7000

# Variables de entorno
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["python", "run.py"]
