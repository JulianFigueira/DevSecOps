FROM python:3.11-slim-bookworm

WORKDIR /app

# Actualizar paquetes del sistema operativo Debian
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no root por seguridad
RUN useradd -m appuser

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Forzar actualización a versiones seguras DESPUÉS de instalar requirements.txt
RUN pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "urllib3>=2.8.0" "msgpack>=1.2.1"

COPY app/ .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
