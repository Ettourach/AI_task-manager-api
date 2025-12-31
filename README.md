# 🚀 Task Manager API

A **modern backend project** built with **Django REST Framework**, featuring JWT authentication, AI-powered task suggestions via OpenAI, and complete API documentation.

---

## 🛠 Badges

| Technology | Badge |
|------------|-------|
| Python     | ![Python](https://img.shields.io/badge/Python-3.13-blue) |
| Django     | ![Django](https://img.shields.io/badge/Django-5.2-green) |
| DRF        | ![DRF](https://img.shields.io/badge/DRF-RESTful-orange) |
| OpenAI     | ![OpenAI](https://img.shields.io/badge/OpenAI-GPT-3.5-purple) |
| License    | ![License](https://img.shields.io/badge/License-MIT-lightgrey) |

---

## ✨ Features

- 📝 Full CRUD operations on **tasks**  
- 🔐 JWT Authentication (Simple JWT)  
- 🤖 AI task suggestion endpoint using **OpenAI GPT-3.5**  
- 📄 API documentation with **Swagger** & **ReDoc**  
- 🛠 Admin panel for managing users and tasks  
- 🆕 Signup / Login / Logout pages for user management  
- 🔧 Recent modifications:
  - Added **AI task suggestion improvements**  
  - Refactored `views.py` for clarity and stability  
  - Added proper **signup/login integration**  
  - Updated **API endpoints table** for clarity
  - **LATEST**: Complete code refactoring with improved quality
    - Fixed duplicate model fields (user/owner)
    - Updated to modern OpenAI ChatCompletion API
    - Added comprehensive error handling and logging
    - Improved authentication and permissions
    - Enhanced test coverage (7 tests)
    - Applied Black code formatting
    - Added environment validation command
    - **Ready for production deployment** 🚀
      - Deployment guides for Heroku, Railway, Docker, AWS, VPS
      - Production-ready Dockerfile and docker-compose.yml
      - Heroku Procfile and runtime.txt
      - Nginx configuration for reverse proxy  

---

## 🌐 API Endpoints

| Feature | Method | URL | Description |
|---------|--------|-----|-------------|
| **Admin Panel** | GET | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Django admin dashboard |
| **Index / Homepage** | GET | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Simple homepage |
| **Signup** | GET / POST | [http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/) | Create a new user account |
| **Login** | GET / POST | [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) | User login page |
| **Logout** | GET | [http://127.0.0.1:8000/accounts/logout/](http://127.0.0.1:8000/accounts/logout/) | Logout current user |
| **API Root** | GET | [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) | Root API endpoint |
| **Tasks List / Create** | GET / POST | [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/) | View all tasks / Create new task |
| **Task Detail** | GET / PUT / PATCH / DELETE | [http://127.0.0.1:8000/api/tasks/<id>/](http://127.0.0.1:8000/api/tasks/<id>/) | Retrieve, update or delete a task |
| **AI Task Suggestion** | POST | [http://127.0.0.1:8000/api/suggest-task/](http://127.0.0.1:8000/api/suggest-task/) | Get AI-generated task suggestions |
| **JWT Obtain Token** | POST | [http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/) | Get access & refresh tokens |
| **JWT Refresh Token** | POST | [http://127.0.0.1:8000/api/token/refresh/](http://127.0.0.1:8000/api/token/refresh/) | Refresh access token |
| **Swagger Docs** | GET | [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/) | Interactive API documentation |
| **ReDoc Docs** | GET | [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) | Beautiful ReDoc documentation |

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

# Copy environment template and configure
cp .env.development .env
# Edit .env and add your settings (especially OPENAI_API_KEY if you want AI features)

# Check environment configuration (optional but recommended)
python manage.py check_env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

---

## 🤖 AI Task Suggestion Example

```bash
curl -X POST http://127.0.0.1:8000/api/suggest-task/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your-jwt-token>" \
-d '{"prompt":"study Django"}'
```

**Response Example:**

```json
{
  "suggestion": "Review Django models and build a small CRUD project."
}
```

---

## 🛠 Tech Stack

**Backend:** Django 5.2, Django REST Framework

**Authentication:** JWT (Simple JWT)

**AI:** OpenAI GPT-3.5

**Docs:** drf-yasg (Swagger & ReDoc)

**Database:** SQLite (default, can switch to PostgreSQL)

**Code Quality:** Black, isort

---

## 📌 Notes

- Make sure `OPENAI_API_KEY` is set in `.env` to use the AI endpoint
- Use `python manage.py check_env` to validate your environment configuration
- All links above are local URLs, accessible when the server runs
- The AI suggestion endpoint requires authentication (JWT token)

---

## 🚀 Deployment

This application is **production-ready** and can be deployed to various platforms:

### Quick Deploy Options

- **Heroku**: `git push heroku main` (see [DEPLOYMENT.md](DEPLOYMENT.md))
- **Railway**: One-click deploy from GitHub
- **Docker**: `docker-compose up -d` 
- **Digital Ocean**: App Platform auto-deploy
- **AWS**: Elastic Beanstalk or ECS
- **VPS**: Traditional server deployment with Nginx

📖 **Full deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions for each platform.

### Deployment Files Included

- ✅ `Procfile` - Heroku/Railway deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `Dockerfile` - Production-ready container image
- ✅ `docker-compose.yml` - Multi-container orchestration
- ✅ `nginx.conf` - Reverse proxy configuration
- ✅ `.dockerignore` - Optimized Docker builds

### Pre-Deployment Checklist

```bash
python manage.py check --deploy  # Check deployment readiness
python manage.py test            # Run all tests
python manage.py collectstatic   # Collect static files
```

---

This project is actively maintained, with recent comprehensive refactoring to improve code quality, security, and maintainability.

---

## 📄 License

This project is licensed under the MIT License.