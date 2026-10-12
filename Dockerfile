# [FIX 5] Imagen base actual y usuario sin privilegios
FROM python:3.12-slim
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app/ .
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/salud')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "app:app"]
