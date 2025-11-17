# Deployment Guide - AI Task Manager API

This guide provides instructions for deploying the AI Task Manager API to various platforms.

## Prerequisites

Before deploying, ensure you have:
- ✅ All tests passing (`python manage.py test`)
- ✅ Environment variables configured
- ✅ Database migrations ready
- ✅ Static files collected

## Quick Deployment Checklist

```bash
# 1. Run pre-deployment checks
python manage.py check --deploy

# 2. Run tests
python manage.py test

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Run migrations (on production database)
python manage.py migrate
```

## Environment Variables for Production

Create a `.env` file based on `.env.example`:

```bash
# Required
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (recommended PostgreSQL for production)
DATABASE_URL=postgres://user:password@host:port/dbname

# Optional - for AI features
OPENAI_API_KEY=your-openai-api-key

# Security (for HTTPS deployments)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set DEBUG=False
   heroku config:set OPENAI_API_KEY='your-openai-key'
   heroku config:set SECURE_SSL_REDIRECT=True
   heroku config:set SESSION_COOKIE_SECURE=True
   heroku config:set CSRF_COOKIE_SECURE=True
   ```

5. **Deploy**
   ```bash
   git push heroku copilot/refactor-and-improve-code:main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

7. **Open App**
   ```bash
   heroku open
   ```

### Option 2: Railway

1. **Install Railway CLI** (or use web interface at railway.app)
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Add PostgreSQL**
   ```bash
   railway add postgresql
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set SECRET_KEY='your-secret-key'
   railway variables set DEBUG=False
   railway variables set OPENAI_API_KEY='your-openai-key'
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Run Migrations**
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

### Option 3: Digital Ocean App Platform

1. **Create Account** at digitalocean.com

2. **Create App from GitHub**
   - Connect your GitHub repository
   - Select branch: `copilot/refactor-and-improve-code`
   - Detect: Python/Django app

3. **Configure Environment**
   - Add environment variables in the App Platform dashboard
   - Add PostgreSQL database component

4. **Set Build Command**
   ```bash
   python manage.py collectstatic --noinput && python manage.py migrate
   ```

5. **Set Run Command**
   ```bash
   gunicorn task_manager.wsgi:application
   ```

6. **Deploy** - App Platform will auto-deploy

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.12 your-app-name
   ```

3. **Create Environment**
   ```bash
   eb create production-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv SECRET_KEY='your-secret-key' DEBUG=False
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

6. **Open App**
   ```bash
   eb open
   ```

### Option 5: Docker + Any Cloud Provider

1. **Create Dockerfile** (if not exists)
   ```dockerfile
   FROM python:3.12-slim
   
   WORKDIR /app
   
   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application
   COPY . .
   
   # Collect static files
   RUN python manage.py collectstatic --noinput
   
   # Expose port
   EXPOSE 8000
   
   # Run gunicorn
   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_manager.wsgi:application"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       environment:
         - SECRET_KEY=${SECRET_KEY}
         - DEBUG=False
         - DATABASE_URL=${DATABASE_URL}
         - OPENAI_API_KEY=${OPENAI_API_KEY}
       depends_on:
         - db
     
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=taskmanager
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

3. **Build and Deploy**
   ```bash
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

### Option 6: Traditional VPS (Ubuntu)

1. **SSH into Server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.12 python3-pip postgresql nginx
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/Ettourach/AI_task-manager-api.git
   cd AI_task-manager-api
   git checkout copilot/refactor-and-improve-code
   ```

4. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createdb taskmanager
   sudo -u postgres createuser taskuser
   ```

6. **Set Environment Variables**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your settings
   ```

7. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

8. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/taskmanager.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Task Manager API
   After=network.target
   
   [Service]
   User=your-user
   Group=www-data
   WorkingDirectory=/path/to/AI_task-manager-api
   Environment="PATH=/path/to/AI_task-manager-api/venv/bin"
   ExecStart=/path/to/AI_task-manager-api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 task_manager.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

9. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/taskmanager
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /path/to/AI_task-manager-api;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

10. **Enable and Start Services**
    ```bash
    sudo systemctl enable taskmanager
    sudo systemctl start taskmanager
    sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled
    sudo systemctl restart nginx
    ```

## Post-Deployment

### 1. Verify Deployment

```bash
# Check if site is accessible
curl https://yourdomain.com/api/

# Check admin panel
curl https://yourdomain.com/admin/

# Check API docs
curl https://yourdomain.com/docs/
```

### 2. Create Admin User

```bash
python manage.py createsuperuser
```

### 3. Monitor Logs

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u taskmanager -f
```

### 4. Setup SSL/HTTPS

Most platforms (Heroku, Railway, DO) provide automatic SSL. For VPS:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

## Environment-Specific Settings

### Development
```bash
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECURE_SSL_REDIRECT=False
```

### Staging
```bash
DEBUG=True
ALLOWED_HOSTS=staging.yourdomain.com
SECURE_SSL_REDIRECT=True
```

### Production
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Connection Issues
```bash
# Check DATABASE_URL format
# PostgreSQL: postgres://user:password@host:port/dbname
```

### Import Errors
```bash
pip install -r requirements.txt
```

### Permission Errors
```bash
# Ensure proper file permissions
chmod -R 755 /path/to/app
```

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS enabled (`SECURE_SSL_REDIRECT=True`)
- [ ] Database password is strong
- [ ] `OPENAI_API_KEY` kept secret
- [ ] Regular backups configured
- [ ] Monitoring and alerts setup

## Scaling Considerations

### Database
- Use managed PostgreSQL (RDS, Heroku Postgres, Railway)
- Enable connection pooling
- Regular backups

### Application
- Use multiple worker processes (gunicorn workers)
- Enable auto-scaling on cloud platforms
- Use CDN for static files

### Caching
- Add Redis for session storage
- Enable Django cache framework
- Use HTTP caching headers

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Run `python manage.py check --deploy`
4. Review this guide's troubleshooting section

---

**Note**: This application is production-ready with all security best practices implemented. Choose the deployment option that best fits your needs and budget.
