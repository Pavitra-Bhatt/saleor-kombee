from .settings import *

# Production settings
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

# Database
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}

# Static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allowed hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Add whitenoise middleware
MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE
