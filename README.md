# Synexify

Minimal Django 5 + PostgreSQL project running in Docker.

---

## Requirements

* Docker ≥ 24
* Docker Compose (built into Docker ≥ 24)
* Linux / macOS / Windows (with WSL or Docker Desktop)

---

## Project Structure

```
Synexify/
├─ appcore/                 # Django configuration
│  ├─ __init__.py
│  ├─ settings.py           
│  ├─ urls.py               
│  ├─ wsgi.py               
│  └─ asgi.py               
├─ Dockerfile
├─ docker-compose.yml
├─ manage.py
├─ .env
├─ .env.example
└─ README.md
```

---

## Environment Setup

1. Copy the example env file:

```bash
cp .env.example .env
```

2. Edit `.env` with your environment variables, e.g.:

```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

---

## Running the Project

1. Build and start containers:

```bash
docker compose up --build
```

2. Open in browser:

```
http://127.0.0.1:8000/
```

You should see the Django default page or your own view.

---

## Database Setup / Migrations

Before creating a superuser or using the admin panel, apply migrations:

```bash
docker compose exec web python manage.py migrate
```

## Superuser / Admin Panel

To access Django admin panel:

```bash
docker compose exec web python manage.py createsuperuser
```

* Open `http://127.0.0.1:8000/admin/`
* Log in with the superuser credentials

---
