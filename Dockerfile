FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=billing_engine.settings

RUN python manage.py collectstatic --noinput || true

CMD ["sh", "-c", "python manage.py migrate && gunicorn billing_engine.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
