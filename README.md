# Synexify

Project Management System implemented in **Python** with **Domain-Driven Design (DDD)** principles.  
Supports projects, sprints, tasks, users, notifications, and reporting.

---

## Requirements

* Docker ≥ 24
* Docker Compose (built into Docker ≥ 24)
* Linux / macOS / Windows (with WSL or Docker Desktop)

---

## Project Structure

```
Synexify/
├─ appcore/                 # Django core configuration
│  ├─ __init__.py
│  ├─ settings.py           
│  ├─ urls.py               
│  ├─ wsgi.py               
│  └─ asgi.py          
├─ domain/                  # Busines domain logic (DDD)
│  ├─ attachments/
│  │  ├─ __init__.py
│  │  ├─ attachment.py
│  ├─ comments/
│  │  ├─ __init__.py
│  │  ├─ comment.py
│  ├─ events/
│  │  ├─ __init__.py
│  │  ├─ base_events.py
│  │  ├─ task_events.py
│  ├─ exceptions/
│  │  ├─ __init__.py
│  │  ├─ exceptions.py
│  ├─ interfaces/
│  │  ├─ __init__.py
│  │  ├─ assignable.py
│  │  ├─ commentable.py
│  │  ├─ reportable.py
│  ├─ projects/
│  │  ├─ __init__.py
│  │  ├─ client_project.py
│  │  ├─ internal_project.py
│  │  ├─ project_base.py
│  ├─ sprints/
│  │  ├─ __init__.py
│  │  ├─ sprint_base.py
│  ├─ tags/
│  │  ├─ __init__.py
│  │  ├─ tag.py
│  ├─ tasks/
│  │  ├─ __init__.py
│  │  ├─ bug_task.py
│  │  ├─ chore_task.py
│  │  ├─ feature_task.py
│  │  ├─ task_base.py
│  ├─ users/
│  │  ├─ __init__.py
│  │  ├─ admin_user.py
│  │  ├─ client_user.py
│  │  ├─ manager_user.py
│  │  ├─ team_member_user.py
│  │  ├─ user_base.py
├─ application/                 # Use-case logic
│  ├─ __init__.py
│  ├─ admin_panel_service.py                     
│  ├─ authorization_service.py                     
│  ├─ backlog_service.py                     
│  ├─ notifications_service.py                     
│  ├─ reporting_service.py                     
│  ├─ sprint_service.py                     
│  └─ task_service.py  
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
