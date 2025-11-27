# 🚀 Task Manager API

A **modern backend project** built with **Django REST Framework**, featuring JWT authentication, AI-powered task suggestions via OpenAI, reminders, dashboard KPIs, and complete API documentation.

---

## 🛠 Badges

| Technology | Badge |
|------------|-------|
| Python     | ![Python](https://img.shields.io/badge/Python-3.12-blue) |
| Django     | ![Django](https://img.shields.io/badge/Django-5.2-green) |
| DRF        | ![DRF](https://img.shields.io/badge/DRF-RESTful-orange) |
| OpenAI     | ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-purple) |
| Celery     | ![Celery](https://img.shields.io/badge/Celery-Async-yellow) |
| License    | ![License](https://img.shields.io/badge/License-MIT-lightgrey) |

---

## ✨ Features

- 📝 Full CRUD operations on **tasks** with tags, due dates, and completion tracking
- 🏷️ **Tags** for categorizing tasks with filtering support
- ⏰ **Reminders** system with management command and Celery task
- 📊 **Dashboard** endpoint with KPIs (completed count, tasks per category, avg completion time, productivity score)
- 🔐 **JWT Authentication** (Simple JWT)
- 🤖 **AI task suggestion** endpoint using **OpenAI GPT-3.5** with fallback to rule-based suggestions
- 👤 **User profiles** with timezone, theme, language, and notification preferences
- 📄 API documentation with **Swagger**, **ReDoc**, and **drf-spectacular**
- 🛠 Admin panel for managing users, tasks, tags, reminders, and profiles
- 🆕 Signup / Login / Logout pages for user management

---

## 🌐 API Endpoints

| Feature | Method | URL | Description |
|---------|--------|-----|-------------|
| **Admin Panel** | GET | `/admin/` | Django admin dashboard |
| **Index / Homepage** | GET | `/` | Simple homepage |
| **API Root** | GET | `/api/` | Root API endpoint |
| **Tasks CRUD** | GET/POST | `/api/tasks/` | List all tasks / Create new task |
| **Task Detail** | GET/PUT/PATCH/DELETE | `/api/tasks/<id>/` | Retrieve, update or delete a task |
| **Tags CRUD** | GET/POST | `/api/tags/` | List all tags / Create new tag |
| **Tag Detail** | GET/PUT/PATCH/DELETE | `/api/tags/<slug>/` | Retrieve, update or delete a tag |
| **Reminders CRUD** | GET/POST | `/api/reminders/` | List/Create reminders |
| **Reminder Detail** | GET/PUT/PATCH/DELETE | `/api/reminders/<id>/` | Manage reminder |
| **Dashboard KPIs** | GET | `/api/dashboard/` | Get productivity metrics |
| **AI Task Suggestion** | POST | `/api/suggest-task/` | Get AI-generated task suggestions |
| **User Profile** | GET/PATCH | `/api/profile/` | Get/Update user profile |
| **JWT Obtain Token** | POST | `/api/token/` | Get access & refresh tokens |
| **JWT Refresh Token** | POST | `/api/token/refresh/` | Refresh access token |
| **Swagger Docs** | GET | `/docs/` | Interactive API documentation (drf-yasg) |
| **ReDoc Docs** | GET | `/redoc/` | ReDoc documentation |
| **API Schema** | GET | `/api/schema/` | OpenAPI schema (drf-spectacular) |
| **API Docs** | GET | `/api/docs/` | Swagger UI (drf-spectacular) |

---

## 🔧 Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Optional - for AI suggestions
OPENAI_API_KEY=your_openai_api_key

# Optional - for Celery (reminders)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Optional - for production database
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

---

## ⚡ Installation & Setup

```bash
# Clone repository
git clone <your-repo-url>
cd task-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Environment Variables section)

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

### Running with Celery (for reminders)

```bash
# Start Redis (required for Celery)
redis-server

# In a new terminal, start Celery worker
celery -A task_manager worker --loglevel=info

# In another terminal, start Celery beat scheduler
celery -A task_manager beat --loglevel=info
```

### Manual reminder processing

```bash
# Process due reminders manually
python manage.py send_reminders

# Dry run (see what would be processed)
python manage.py send_reminders --dry-run
```

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api
python manage.py test users
python manage.py test ai

# Run with verbosity
python manage.py test -v 2
```

---

## 🤖 AI Task Suggestion Example

```bash
curl -X POST http://127.0.0.1:8000/api/suggest-task/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{"prompt":"study Django"}'
```

Response Example:
```json
{
  "suggestion": "Review Django models and build a small CRUD project.",
  "used_openai": true
}
```

**Note:** If `OPENAI_API_KEY` is not set, the endpoint uses rule-based suggestions.

---

## 📊 Dashboard Example

```bash
curl http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer <your_jwt_token>"
```

Response Example:
```json
{
  "completed_count": 15,
  "tasks_per_category": [
    {"tags__name": "Work", "count": 10},
    {"tags__name": "Personal", "count": 5}
  ],
  "avg_completion_time": 86400.0,
  "productivity_score": 75.0
}
```

---

## 🖥️ Frontend

A React frontend scaffolding is provided in the `frontend/` directory. See `frontend/README.md` for setup instructions.

---

## 🛠 Tech Stack

- **Backend:** Django 5.2, Django REST Framework
- **Authentication:** JWT (Simple JWT)
- **AI:** OpenAI GPT-3.5 (with fallback)
- **Task Queue:** Celery + Redis
- **Docs:** drf-yasg (Swagger & ReDoc), drf-spectacular
- **Database:** SQLite (default), PostgreSQL (production)
- **Frontend:** React + Vite + Tailwind CSS (scaffolding)

---

## 📌 Notes

- Make sure `OPENAI_API_KEY` is set in `.env` to use the AI endpoint with OpenAI.
- All authenticated endpoints require a valid JWT token.
- Rate limiting is applied to the AI suggestion endpoint (5 requests/minute).
- Celery requires Redis for the broker and result backend.

---

## 📄 License

This project is licensed under the MIT License.
