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
X_FRAME_OPTIONS = 'DENY'

# Database configuration for production
# Use environment variables for database configuration
if os.getenv('DATABASE_URL'):
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(
                os.getenv('DATABASE_URL'), 
                conn_max_age=300,
                conn_health_checks=True
            )
        }
        # Ensure SSL and IPv4 preference for Supabase
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 30,
            'options': '-c default_transaction_isolation=read_committed',
        }
    except ImportError:
        # Fallback to manual configuration if dj_database_url is not available
        pass
elif all([
    os.getenv("SUPABASE_DB_HOST"),
    os.getenv("SUPABASE_DB_PASSWORD"),
]):
    # Try connection pooler first if available
    db_host = os.getenv("SUPABASE_DB_HOST")
    db_port = os.getenv("SUPABASE_DB_PORT", "5432")
    
    # Check if we should use connection pooler for Vercel
    if os.getenv('VERCEL') and 'supabase.co' in db_host:
        # Try to use connection pooler if available
        pooler_host = db_host.replace('db.', 'aws-0-us-east-1.pooler.')
        if pooler_host != db_host:
            logger.info(f"Attempting to use Supabase pooler: {pooler_host}")
            db_host = pooler_host
            db_port = "6543"  # Default pooler port
    
    # Use PostgreSQL if environment variables are available
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("SUPABASE_DB_NAME", "postgres"),
            'USER': os.getenv("SUPABASE_DB_USER", "postgres"),
            'PASSWORD': os.getenv("SUPABASE_DB_PASSWORD"),
            'HOST': db_host,  
            'PORT': db_port,
            'OPTIONS': {
                'connect_timeout': 30,
                'sslmode': 'require',
                'options': '-c default_transaction_isolation=read_committed',
                # Force IPv4 to avoid IPv6 connectivity issues on Vercel
                'target_session_attrs': 'read-write',
            },
            'CONN_MAX_AGE': 300,  # Reduced connection age for better reliability
            'CONN_HEALTH_CHECKS': True,  # Enable connection health checks
        }
    }
else:
    # If no database environment variables are set, fall back to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
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
