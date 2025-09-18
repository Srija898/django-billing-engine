# Django Billing Engine (Production-Ready Starter)

A batteries-included Django billing engine with **role-based access**, **REST API (DRF + JWT)**,
**periodic billing via Celery**, **tests**, **Docker deployment**, and **CI**.

## Features
- Plans, Customers, Subscriptions, Invoices, Invoice Items, Payments
- Role-based access using Django Groups: `Admin`, `Finance`, `Support`, `Developer`, `Customer`
- JWT auth (access/refresh) with DRF
- Admin configured for key models
- Celery worker + beat for scheduled invoice generation
- Postgres + Redis in `docker-compose.yml`
- Seed script to create default roles and permissions
- Tests (models + API smoke)
- GitHub Actions CI (lint, tests)
- Twelve-Factor settings via environment variables

## Quickstart (Local, SQLite)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_roles
python manage.py runserver
```
JWT:
```bash
# get token
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"<user>","password":"<pass>"}'
```

## Docker (Postgres + Redis + Celery + Gunicorn)
```bash
cp .env.example .env
docker compose up --build
# Django at http://localhost:8000
```
Celery worker & beat are included. To create roles:
```bash
docker compose exec web python manage.py seed_roles
```

## API (selected)
- `/api/plans/` CRUD (Admin/Finance: full; Support: read; Customer: read)
- `/api/customers/` CRUD (Admin/Finance: full; Support: read; Customer: self-read)
- `/api/subscriptions/` CRUD guarded by roles
- `/api/invoices/` read + create via task; payments recorded via `/api/payments/`
- JWT: `/api/token/`, `/api/token/refresh/`

## Tests
```bash
pytest -q
# or
python manage.py test
```

## Deployment
- Containerized with Gunicorn, WhiteNoise, and environment-driven settings.
- Provide `SECRET_KEY`, `ALLOWED_HOSTS`, and Postgres/Redis URLs.
- Run migrations and `seed_roles` once after deploy.
- Example Proc:
```bash
gunicorn billing_engine.wsgi:application --bind 0.0.0.0:$PORT --workers 3
celery -A billing_engine worker -l info
celery -A billing_engine beat -l info
```

## Env Vars
See `.env.example` for all options. Key ones:
- `SECRET_KEY` (required in prod)
- `DEBUG` (`0` or `1`)
- `ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (e.g., postgres://user:pass@db:5432/app)
- `REDIS_URL` (e.g., redis://redis:6379/0)
- `TIME_ZONE` (default: UTC)

## License
MIT
