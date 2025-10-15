🧠 AI Task Manager API
An intelligent Task Management API built with Django REST Framework and OpenAI API, designed to help users create, manage, and get AI-generated task suggestions.

🚀 Features
✅ Create, Read, Update, Delete (CRUD) tasks
🤖 Generate task ideas using OpenAI API
👤 User-linked task management
🧩 RESTful endpoints with Django REST Framework
🌐 Ready for cloud deployment (Render, Railway, etc.)
🧱 Project Structure
AI_task-manager-api/ ├── api/ # App (models, serializers, views) ├── task_manager/ # Django project settings ├── manage.py # Django management script ├── requirements.txt # Dependencies ├── Procfile # Deployment entrypoint ├── .env # Environment variables └── README.md # Documentation

yaml Copy code

⚙️ Local Setup Guide
Follow these steps to run the project locally 👇

1️⃣ Clone the repository
git clone https://github.com/Ettourach/AI_task-manager-api.git
cd AI_task-manager-api
2️⃣ Create and activate a virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Create a .env file in the project root
bash
Copy code
DJANGO_SECRET_KEY=your-generated-secret-key
OPENAI_API_KEY=your-openai-api-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
5️⃣ Run migrations and create a superuser
bash
Copy code
python manage.py migrate
python manage.py createsuperuser
6️⃣ Start the local server
bash
Copy code
python manage.py runserver
➡ Access the API at: http://127.0.0.1:8000/api/tasks/
➡ Admin panel: http://127.0.0.1:8000/admin/

🧠 API Endpoints
Method	Endpoint	Description
GET	/api/tasks/	List all tasks
POST	/api/tasks/	Create a new task
GET	/api/tasks/<id>/	Retrieve a specific task
PUT	/api/tasks/<id>/	Update an existing task
DELETE	/api/tasks/<id>/	Delete a task
POST	/api/tasks/suggest/	Get AI-generated task suggestion

🌍 Deployment (Optional)
If deploying to Render or Railway, make sure you have these files in your root:
✅ Procfile
✅ requirements.txt
✅ .env
Example Render settings:
Build Command: pip install -r requirements.txt

Start Command: gunicorn task_manager.wsgi

👨‍💻 Author
Ilyas Ettourach

🌐 GitHub: @Ettourach

💼 LinkedIn: in/ilyas-ettourach-8b2714146

🐦 Twitter: @IEttourach

🧾 License
This project is licensed under the MIT License.

yaml
Copy code

---

### ✅ Next step:
In your root directory:
```bash
echo "# AI Task Manager API" > README.md