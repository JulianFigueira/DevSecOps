FROM python:3.11-slim-bookworm

WORKDIR /app

# Actualizar paquetes del sistema operativo Debian
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no root por seguridad
RUN useradd -m appuser

# Actualizar herramientas base y dependencias con vulnerabilidades reportadas por Trivy
RUN pip install --no-cache-dir --upgrade pip "setuptools>=78.1.1" "urllib3>=2.8.0" "msgpack>=1.2.1"

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
