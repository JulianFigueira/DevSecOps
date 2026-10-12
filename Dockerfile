FROM python:3.11-slim-bookworm

WORKDIR /app

# Crear usuario no root por seguridad
RUN useradd -m appuser

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
