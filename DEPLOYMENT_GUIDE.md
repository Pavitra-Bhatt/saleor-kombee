# Saleor Deployment Guide - Free Hosting Services

This guide will help you deploy your Saleor application to free hosting services.

## 🚀 Quick Start Options

### Option 1: Railway (Recommended - Easiest)
Railway is the easiest option with automatic deployments from GitHub.

### Option 2: Render
Render offers free hosting with automatic deployments.

### Option 3: Heroku
Heroku has a free tier (with limitations) and good Django support.

## 📋 Pre-Deployment Checklist

### 1. Prepare Your Application

```bash
# Create Procfile
echo "web: gunicorn saleor.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Generate requirements.txt
pip freeze > requirements.txt

# Add essential packages
echo "gunicorn>=20.1.0" >> requirements.txt
echo "psycopg2-binary>=2.9.0" >> requirements.txt
echo "dj-database-url>=2.0.0" >> requirements.txt
echo "whitenoise>=6.0.0" >> requirements.txt
```

### 2. Update Settings for Production

Create a new file `saleor/settings_production.py`:

```python
from .settings import *

# Production settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allowed hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Add whitenoise middleware
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

## 🚂 Railway Deployment

### Step 1: Sign Up
1. Go to [Railway.app](https://railway.app/)
2. Sign up with your GitHub account

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your Saleor repository

### Step 3: Configure Environment Variables
Add these environment variables in Railway dashboard:

```
DATABASE_URL=postgresql://neondb_owner:npg_duhKJB6AIC0o@ep-curly-tree-a1i1u69o-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
```

### Step 4: Deploy
Railway will automatically deploy your application. You can monitor the deployment in the dashboard.

## 🎨 Render Deployment

### Step 1: Sign Up
1. Go to [Render.com](https://render.com/)
2. Sign up with your GitHub account

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: saleor-store
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn saleor.wsgi:application`

### Step 3: Configure Environment Variables
Add these environment variables:

```
DATABASE_URL=postgresql://neondb_owner:npg_duhKJB6AIC0o@ep-curly-tree-a1i1u69o-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Step 4: Deploy
Render will automatically deploy your application.

## 🦸 Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# macOS
brew install heroku/brew/heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App
```bash
heroku login
heroku create your-saleor-app-name
```

### Step 3: Add PostgreSQL Add-on
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Configure Environment Variables
```bash
heroku config:set SECRET_KEY=your-generated-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

### Step 5: Deploy
```bash
git push heroku main
```

## 🔧 Post-Deployment Steps

### 1. Run Migrations
```bash
# Railway
railway run python manage.py migrate

# Render
# Add to build command: && python manage.py migrate

# Heroku
heroku run python manage.py migrate
```

### 2. Create Superuser
```bash
# Railway
railway run python manage.py createsuperuser

# Render
# Add to build command: && python manage.py createsuperuser

# Heroku
heroku run python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
# Railway
railway run python manage.py collectstatic --noinput

# Render
# Add to build command: && python manage.py collectstatic --noinput

# Heroku
heroku run python manage.py collectstatic --noinput
```

## 🔐 Security Considerations

### 1. Generate Secret Key
```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
print(secret_key)
```

### 2. Environment Variables
Never commit sensitive information to your repository. Use environment variables for:
- `SECRET_KEY`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- API keys and passwords

### 3. SSL/HTTPS
All recommended platforms provide SSL certificates automatically.

## 📊 Monitoring and Maintenance

### 1. Logs
- **Railway**: View logs in the dashboard
- **Render**: View logs in the dashboard
- **Heroku**: `heroku logs --tail`

### 2. Database Backups
- Set up regular backups for your Neon database
- Consider using Neon's built-in backup features

### 3. Performance Monitoring
- Monitor your application's performance
- Set up alerts for downtime

## 🆘 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check if all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Database Connection Issues**:
   - Ensure `DATABASE_URL` is correctly set
   - Check if Neon database is accessible

3. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` configuration

4. **500 Errors**:
   - Check application logs
   - Verify environment variables are set correctly

### Getting Help

- **Railway**: [Discord Community](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Heroku**: [Support](https://help.heroku.com/)

## 🎯 Recommended Setup

For the easiest deployment experience, I recommend:

1. **Railway** for hosting (easiest setup)
2. **Neon** for database (already configured)
3. **GitHub** for version control

This combination provides:
- Free hosting with automatic deployments
- Serverless PostgreSQL database
- Easy environment variable management
- Built-in SSL certificates
- Good performance for development and small projects
