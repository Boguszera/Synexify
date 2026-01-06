# Synexify

Project Management System implemented in **Python** with **Domain-Driven Design (DDD)** principles.  
Supports projects, sprints, tasks, users, notifications, comments, attachments and reporting.

---

## Requirements

* Docker ≥ 24
* Docker Compose (built into Docker ≥ 24)
* Linux / macOS / Windows (with WSL or Docker Desktop)
* Git

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Boguszera/Synexify.git
cd Synexify
```

### 2. Create Environment File

```bash
cp .env.example . env
```

### 3. Configure Environment Variables

Edit `.env` with your settings:

```bash
# Django Settings
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=synexify_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

---

## Running the Project

### 1. Build and Start Containers

```bash
docker compose up --build
```

This will: 
- Build the Django application container
- Start PostgreSQL database container
- Run migrations automatically
- Start the development server on port 8000

### 2. Access the Application

- **Web Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/

---

## Seeding the Database

### Create Sample Data

```bash
docker compose exec web python manage.py seed
```

This creates:  

#### 👥 **Demo Users** (Password: `demo123`)

| Login | Role                    | Email | 
|-------|-------------------------|-------|
| `root` | Admin                   | root@demo.synexify.com |
| `manager1` | Manager                 | manager1@demo.synexify.com |
| `dev1` | Developer (Team Member) | dev1@demo.synexify.com |
| `dev2` | Developer (Team Member) | dev2@demo.synexify.com | 
| `qa1` | QA (Team Member)                     | qa1@demo.synexify.com |
| `client1` | Client                  | client1@demo.synexify.com |

#### 📦 **Sample Data**

- **3 Projects**:  WebApp Rebuild, Mobile CRM Platform, Marketing Landing Page
- **3 Active Sprints**: With different stages and task loads
- **14 Tasks**: Mix of Features (with story points), Bugs (with severity), and Chores (basic task)
- **7 Tags**: backend, frontend, api, ux, urgent, review, devops
- **6 Comments**: Team collaboration examples

---

## Admin Panel & Superuser

### Create Admin User

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to create a new admin account.

### Access Django Admin

1. Open http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials

---

## API Endpoints

### Authentication

```bash
# Login
POST /api/auth/login/
{
  "username": "dev1",
  "password": "demo123"
}

# Refresh Token
POST /api/auth/refresh/
{
  "refresh": "token_here"
}
```

### Projects

```bash
GET    /api/projects/              # List all projects
POST   /api/projects/              # Create new project
GET    /api/projects/{id}/         # Get project details
PATCH  /api/projects/{id}/         # Update project
DELETE /api/projects/{id}/         # Delete project
```

### Sprints

```bash
GET    /api/sprints/               # List all sprints
POST   /api/sprints/               # Create sprint
GET    /api/sprints/{id}/          # Get sprint details
PATCH  /api/sprints/{id}/          # Update sprint
DELETE /api/sprints/{id}/          # Delete sprint
POST   /api/sprints/{id}/add_task/ # Add task to sprint
GET    /api/sprints/{id}/tasks/    # Get sprint tasks
```

### Tasks

```bash
GET    /api/tasks/                 # List all tasks
POST   /api/tasks/                 # Create task
GET    /api/tasks/{id}/            # Get task details
PATCH  /api/tasks/{id}/            # Update task
DELETE /api/tasks/{id}/            # Delete task
PATCH  /api/tasks/{id}/assign/     # Assign user
POST   /api/tasks/{id}/add_comment/        # Add comment
GET    /api/tasks/{id}/comments/   # Get comments
POST   /api/tasks/{id}/add_attachment/     # Upload file
GET    /api/tasks/{id}/attachments/# Get attachments
```

### Reports

```bash
GET /api/reporting/dashboard/      # Dashboard overview
GET /api/reports/status/           # Task status summary
GET /api/reports/workload/         # Team workload
GET /api/reports/velocity/         # Team velocity
```

---

## Key Features by Role

### 👨‍💼 **Admin**
- Manage all users
- Manage all projects
- Access all reports
- System configuration

### 👔 **Manager**
- Create & manage projects
- Plan sprints
- Assign tasks
- View team workload
- Generate reports

### 👨‍💻 **Developer**
- View assigned tasks
- Update task status
- Add comments
- Upload attachments
- Track progress

### 🎯 **QA**
- Report bugs
- Add comments to tasks
- Update task status
- Test features

### 👥 **Client**
- View assigned projects
- Track progress
- Add comments
- View reports (limited)

---

## Database Schema

The system uses PostgreSQL with the following main entities:

- **Users** - User accounts with roles
- **Projects** - Project organization
- **Sprints** - Sprint planning containers
- **Tasks** - Work items (Features, Bugs, Chores)
- **Comments** - Task discussions
- **Attachments** - File uploads
- **Tags** - Task categorization
- **Notifications** - User notifications

---

## Development

### Create Migrations

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage. py migrate
```

### Access Django Shell

```bash
docker compose exec web python manage.py shell
```

### View Logs

```bash
docker compose logs -f web
docker compose logs -f db
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Restart database
docker compose down
docker compose up -d db
docker compose up web
```

### Permission Denied Errors

```bash
# Check file permissions
docker compose exec web chmod -R 755 /app/media/
```

### Clear Cache & Rebuild

```bash
docker compose down -v  # Remove all volumes
docker compose up --build
```

---

## Technology Stack

- **Backend**: Django 5.2, Python 3.12
- **Database**: PostgreSQL 16
- **API**: Django REST Framework with JWT
- **Architecture**: Domain-Driven Design (DDD)
- **Containerization**: Docker & Docker Compose
- **Frontend**: Bootstrap 5

---

## Architecture Principles

This project follows **Domain-Driven Design (DDD)**:

- **Domain Layer** (`domain/`) - Pure business logic
- **Application Layer** (`application/`) - Use cases
- **Infrastructure Layer** (`infrastructure/`) - Technical implementation
- **Presentation Layer** (`api/`, `web/`) - User interfaces

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues and questions:   
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation in code comments

---

## Author

**Boguszera** - Project Creator

---
