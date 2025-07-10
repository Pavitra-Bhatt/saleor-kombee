#!/usr/bin/env python3
"""
Script to prepare Saleor for deployment
"""

import os
import subprocess
import sys
import secrets
import string


def create_procfile():
    """Create Procfile for deployment"""
    procfile_content = """web: gunicorn saleor.wsgi:application --bind 0.0.0.0:$PORT
"""

    with open("Procfile", "w") as f:
        f.write(procfile_content)

    print("✓ Created Procfile")


def create_runtime_txt():
    """Create runtime.txt with Python version"""
    runtime_content = """python-3.11.0
"""

    with open("runtime.txt", "w") as f:
        f.write(runtime_content)

    print("✓ Created runtime.txt")


def update_requirements():
    """Update requirements.txt"""
    try:
        # Generate requirements.txt
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True,
        )

        requirements = result.stdout

        # Add essential packages if not present
        essential_packages = [
            "gunicorn>=20.1.0",
            "psycopg2-binary>=2.9.0",
            "dj-database-url>=2.0.0",
            "whitenoise>=6.0.0",  # For static files
        ]

        for package in essential_packages:
            if package.split(">=")[0] not in requirements:
                requirements += f"\n{package}\n"

        with open("requirements.txt", "w") as f:
            f.write(requirements)

        print("✓ Updated requirements.txt")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error updating requirements.txt: {e}")
        return False


def create_env_example():
    """Create .env.example file"""
    env_example_content = """# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_CLIENT_HOSTS=your-domain.com

# Email Settings (optional)
EMAIL_URL=smtp://localhost:1025

# Redis Settings (optional)
REDIS_URL=redis://localhost:6379/0

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
"""

    with open(".env.example", "w") as f:
        f.write(env_example_content)

    print("✓ Created .env.example")


def generate_secret_key():
    """Generate a new Django secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = "".join(secrets.choice(alphabet) for i in range(50))

    print(f"Generated SECRET_KEY: {secret_key}")
    return secret_key


def check_git_status():
    """Check if git repository is properly set up"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Git repository is ready")
            return True
        else:
            print("✗ Git repository not found or not initialized")
            return False
    except FileNotFoundError:
        print("✗ Git not installed")
        return False


def main():
    print("🚀 Preparing Saleor for Deployment")
    print("=" * 40)

    # Create necessary files
    create_procfile()
    create_runtime_txt()
    update_requirements()
    create_env_example()

    # Check git status
    git_ready = check_git_status()

    # Generate secret key
    secret_key = generate_secret_key()

    print("\n📋 Deployment Checklist:")
    print("1. ✅ Procfile created")
    print("2. ✅ runtime.txt created")
    print("3. ✅ requirements.txt updated")
    print("4. ✅ .env.example created")
    print("5. ✅ settings_production.py created")
    print(f"6. {'✅' if git_ready else '❌'} Git repository ready")
    print("7. ✅ Secret key generated")

    print("\n🎯 Next Steps:")
    print("1. Push your code to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for deployment'")
    print("   git push origin main")

    print("\n2. Choose your deployment platform:")
    print("   - Railway: https://railway.app/ (Recommended)")
    print("   - Render: https://render.com/")
    print("   - Heroku: https://heroku.com/")

    print("\n3. Set environment variables:")
    print(f"   SECRET_KEY={secret_key}")
    print(
        "   DATABASE_URL=postgresql://neondb_owner:npg_duhKJB6AIC0o@ep-curly-tree-a1i1u69o-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    print("   DEBUG=False")
    print("   ALLOWED_CLIENT_HOSTS=your-app-name.railway.app")

    print("\n4. Deploy and run migrations:")
    print("   python manage.py migrate")
    print("   python manage.py collectstatic")


if __name__ == "__main__":
    main()
