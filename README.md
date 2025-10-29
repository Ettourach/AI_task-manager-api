# 🚀 Task Manager API

A **modern backend project** built with **Django REST Framework**, featuring JWT authentication, AI-powered task suggestions via OpenAI, and complete API documentation.  

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-RESTful-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-3.5-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Features

- 📝 Full CRUD operations on tasks  
- 🔐 JWT Authentication (Simple JWT)  
- 🤖 AI task suggestion endpoint using **OpenAI GPT-3.5**  
- 📄 API documentation with **Swagger** & **ReDoc**  
- 🛠 Admin panel for managing users and tasks  

---

## 🌐 API Endpoints

| Feature | Method | URL | Description |
|---------|--------|-----|-------------|
| **Admin Panel** | GET | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Django admin dashboard |
| **Index / Homepage** | GET | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Simple homepage |
| **API Root** | GET | [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) | Root API endpoint |
| **Tasks List / Create** | GET / POST | [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/) | View all tasks / Create new task |
| **Task Detail** | GET / PUT / PATCH / DELETE | [http://127.0.0.1:8000/api/tasks/<id>/](http://127.0.0.1:8000/api/tasks/<id>/) | Retrieve, update or delete a task |
| **AI Task Suggestion** | POST | [http://127.0.0.1:8000/api/suggest-task/](http://127.0.0.1:8000/api/suggest-task/) | Get AI-generated task suggestions |
| **JWT Obtain Token** | POST | [http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/) | Get access & refresh tokens |
| **JWT Refresh Token** | POST | [http://127.0.0.1:8000/api/token/refresh/](http://127.0.0.1:8000/api/token/refresh/) | Refresh access token |
| **Swagger Docs** | GET | [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/) | Interactive API docs |
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

# Create .env file with your environment variables
echo SECRET_KEY='your_secret_key' >> .env
echo DEBUG=True >> .env
echo ALLOWED_HOSTS='127.0.0.1,localhost' >> .env
echo OPENAI_API_KEY='your_openai_api_key' >> .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
🤖 AI Task Suggestion Example
bash
curl -X POST http://127.0.0.1:8000/api/suggest-task/ \
-H "Content-Type: application/json" \
-d '{"prompt":"study Django"}'

Response Example:
json

{
  "suggestion": "Review Django models and build a small CRUD project."
}
🛠 Tech Stack
Backend: Django 5.2, Django REST Framework

Authentication: JWT (Simple JWT)

AI: OpenAI GPT-3.5

Docs: drf-yasg (Swagger & ReDoc)

Database: SQLite (default, can switch to PostgreSQL)

📌 Notes
Make sure OPENAI_API_KEY is set in .env to use the AI endpoint.

All links above are local URLs, accessible when the server runs.

📄 License
This project is licensed under the MIT License.