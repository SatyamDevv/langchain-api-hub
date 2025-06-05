"""
Production settings for service_hub project.
This file contains settings specifically for Vercel deployment.
"""

from .settings import *
import os
import logging

logger = logging.getLogger(__name__)

# Production-specific settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Add Vercel domain to allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.satyamdev.me']

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# CSRF settings for production
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True

# Additional security headers
SECURE_SSL_REDIRECT = not DEBUG
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database configuration for production
# Supabase PostgreSQL Configuration
def get_supabase_database_config():
    """Configure Supabase database with proper connection pooling and SSL"""
    
    # First priority: Use DATABASE_URL if provided (standard for many platforms)
    if os.getenv('DATABASE_URL'):
        try:
            import dj_database_url
            config = dj_database_url.parse(
                os.getenv('DATABASE_URL'), 
                conn_max_age=60,  # Shorter for serverless
                conn_health_checks=True
            )
            # Ensure proper SSL and connection options for Supabase
            config['OPTIONS'] = {
                'sslmode': 'require',
                'connect_timeout': 10,
                'application_name': 'django_vercel_app',
                'options': '-c default_transaction_isolation=read_committed -c timezone=UTC',
            }
            return config
        except ImportError:
            logger.warning("dj_database_url not available, falling back to manual config")
    
    # Second priority: Manual Supabase configuration
    if all([
        os.getenv("SUPABASE_DB_HOST"),
        os.getenv("SUPABASE_DB_PASSWORD"),
    ]):
        db_host = os.getenv("SUPABASE_DB_HOST")
        db_port = os.getenv("SUPABASE_DB_PORT", "5432")
        
        # Use connection pooler for production (recommended for serverless)
        if os.getenv('VERCEL') or os.getenv('RAILWAY_ENVIRONMENT'):
            # Auto-detect and use Supabase connection pooler
            if 'supabase.co' in db_host and 'db.' in db_host:
                # Replace db. with aws-0-us-east-1.pooler. for US East region
                # You may need to adjust the region based on your Supabase project
                pooler_host = db_host.replace('db.', 'aws-0-us-east-1.pooler.')
                logger.info(f"Using Supabase connection pooler: {pooler_host}")
                db_host = pooler_host
                db_port = "6543"  # Default pooler port
        
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("SUPABASE_DB_NAME", "postgres"),
            'USER': os.getenv("SUPABASE_DB_USER", "postgres"),
            'PASSWORD': os.getenv("SUPABASE_DB_PASSWORD"),
            'HOST': db_host,
            'PORT': db_port,
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 10,
                'application_name': 'django_vercel_app',
                'options': '-c default_transaction_isolation=read_committed -c timezone=UTC',
                'keepalives_idle': 600,
                'keepalives_interval': 30,
                'keepalives_count': 3,
            },
            'CONN_MAX_AGE': 60,  # Short-lived connections for serverless
            'CONN_HEALTH_CHECKS': True,
        }
    
    # Fallback to SQLite for development
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Set the database configuration
DATABASES = {
    'default': get_supabase_database_config()
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Use WhiteNoise for static files serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure WhiteNoise is in middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'ai_services': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
