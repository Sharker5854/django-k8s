FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py .
COPY README.md .
COPY django_app/ ./django_app/
COPY django-app-chart/ ./django-app-chart/
COPY k8s_manifests/ ./k8s_manifests/
COPY .github/ ./.github/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uvicorn", "django_app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]