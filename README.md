# 🧠 Task Manager API

A powerful backend API built with **Django 5.2**, **Django REST Framework**, and **JWT Authentication**.  
This project lets users manage their tasks, authenticate securely, and even get **AI-powered task suggestions**.

---

## 🚀 Features

✅ User Registration and Login (JWT Authentication)  
✅ Create, Read, Update, Delete (CRUD) tasks  
✅ Filter and search tasks by status or due date  
✅ AI Task Suggestion endpoint using OpenAI API  
✅ Auto-generated Swagger and Redoc API Documentation  
✅ Environment variable configuration using `.env`  
✅ Production-ready setup (Whitenoise, dj-database-url)

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Django 5.2 |
| API Framework | Django REST Framework |
| Authentication | Simple JWT |
| Database | SQLite / PostgreSQL |
| AI Integration | OpenAI API |
| Deployment Ready | Whitenoise, dj-database-url |
| Documentation | drf-yasg (Swagger / Redoc) |

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Ettourach/task-manager-api.git
cd task-manager-api
2️⃣ Create and activate a virtual environment
bash
Copy code
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Create your .env file
Use the example below 👇

ini
Copy code
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
OPENAI_API_KEY=your-openai-api-key
ALLOWED_HOSTS=127.0.0.1,localhost
5️⃣ Apply migrations and run the server
bash
Copy code
python manage.py migrate
python manage.py runserver
Your API will be available at 👉 http://127.0.0.1:8000

🔑 Authentication
The API uses JWT tokens for authentication.

Get token:

bash
Copy code
POST /api/token/
Refresh token:

swift
Copy code
POST /api/token/refresh/
Use the token in your headers:

makefile
Copy code
Authorization: Bearer <your_access_token>
🧠 AI Task Suggestion (Optional Feature)
You can generate smart task suggestions using OpenAI’s API.

Endpoint:
bash
Copy code
POST /api/suggest-task/
Body:
json
Copy code
{
  "prompt": "learn Django REST Framework"
}
Response:
json
Copy code
{
  "suggestion": "Build a REST API for a note-taking app"
}
📚 API Documentation
You can explore all endpoints visually with Swagger or Redoc:

Tool	URL
Swagger UI	http://127.0.0.1:8000/docs/
Redoc	http://127.0.0.1:8000/redoc/

🧪 Run Tests
bash
Copy code
python manage.py test
🧰 Project Structure
bash
Copy code
task-manager-api/
│
├── api/                 # Main app (models, views, serializers)
├── task_manager/        # Project configuration
├── templates/           # HTML templates (if any)
├── staticfiles/         # Static assets
├── .env.example         # Example environment variables
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
🧑‍💻 Author
Ilyas Ettourach
📧 ettourach@gmail.com
🌐 GitHub
💼 LinkedIn
🐦 Twitter

🛡️ License
This project is licensed under the MIT License — feel free to use, modify, and share.