# Contributing to AI Task Manager API

Thank you for your interest in contributing to the AI Task Manager API! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Virtual environment tool (venv)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/AI_task-manager-api.git
   cd AI_task-manager-api
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.development .env
   # Edit .env with your settings
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Tests**
   ```bash
   python manage.py test
   ```

8. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## 📝 Development Guidelines

### Code Style

This project uses **Black** for code formatting and follows **PEP 8** guidelines.

**Before committing, format your code:**
```bash
black api/ task_manager/*.py manage.py
```

**Check your code:**
```bash
python manage.py check
python manage.py check --deploy  # Check production readiness
```

### Testing

**Always write tests for new features:**

```python
# In api/tests.py
class MyNewFeatureTestCase(TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_feature_works(self):
        # Test your feature
        self.assertEqual(expected, actual)
```

**Run tests:**
```bash
python manage.py test
python manage.py test api.tests.MyNewFeatureTestCase  # Run specific test
```

### Environment Validation

Use the built-in environment checker:
```bash
python manage.py check_env
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add task priority field to model
fix: Resolve authentication issue in suggest_task endpoint
docs: Update README with new API endpoints
refactor: Improve error handling in views
test: Add tests for task filtering
```

### Pull Request Process

1. **Create a branch** for your feature/fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Run tests and formatting**
   ```bash
   python manage.py test
   black api/ task_manager/*.py
   python manage.py check
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Your descriptive message"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request** on GitHub with:
   - Clear description of changes
   - Related issue numbers (if applicable)
   - Screenshots (for UI changes)
   - Test results

## 🏗️ Project Structure

```
AI_task-manager-api/
├── api/                      # Main API application
│   ├── management/          # Custom management commands
│   │   └── commands/
│   │       └── check_env.py # Environment validation
│   ├── migrations/          # Database migrations
│   ├── admin.py            # Admin interface configuration
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── tests.py            # Test suite
│   ├── urls.py             # API URL routing
│   ├── utils.py            # Utility functions
│   └── views.py            # API views and logic
├── task_manager/            # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── templates/               # HTML templates
├── .env.development         # Development environment template
├── .env.example            # Production environment template
├── .gitignore              # Git ignore rules
├── CHANGELOG.md            # Change history
├── CONTRIBUTING.md         # This file
├── README.md               # Project documentation
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

- Python version
- Django version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces
- Screenshots (if applicable)

## 💡 Feature Requests

Feature requests are welcome! Please:

- Check existing issues first
- Describe the feature clearly
- Explain the use case
- Consider implementation details

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## ❓ Questions?

Feel free to open an issue for questions or clarifications!

---

Thank you for contributing! 🎉
