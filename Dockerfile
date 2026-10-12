FROM python:3.11-slim-bookworm

WORKDIR /app

# Actualizar paquetes del sistema operativo Debian para corregir vulnerabilidades
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no root por seguridad
RUN useradd -m appuser

# Actualizar pip y setuptools para eliminar vulnerabilidades de herramientas base
RUN pip install --no-cache-dir --upgrade pip setuptools

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
