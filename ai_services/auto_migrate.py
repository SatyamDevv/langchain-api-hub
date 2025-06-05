import os
from django.core.management import execute_from_command_line
from django.http import JsonResponse
import threading
import logging

logger = logging.getLogger(__name__)

class AutoMigrateMiddleware:
    """
    Middleware to automatically run migrations on first request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.migration_lock = threading.Lock()
        self.migrations_run = False

    def __call__(self, request):
        # Run migrations on first request if not already done
        if not self.migrations_run and not request.path.startswith('/static/'):
            self.run_migrations()
          response = self.get_response(request)
        return response

    def run_migrations(self):
        """Run database migrations safely"""
        with self.migration_lock:
            if self.migrations_run:
                return
            
            try:
                logger.info("Running database migrations...")
                
                # Set the settings module based on environment
                if not os.environ.get('DJANGO_SETTINGS_MODULE'):
                    if os.getenv('VERCEL'):
                        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_hub.production_settings')
                    else:
                        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_hub.settings')
                
                # Test database connection first
                from django.db import connection
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT 1")
                    logger.info("Database connection successful")
                except Exception as db_error:
                    logger.error(f"Database connection failed: {str(db_error)}")
                    self.migrations_run = True  # Prevent retry on every request
                    return
                
                # Run migrations with safer options
                try:
                    execute_from_command_line(['manage.py', 'migrate', '--verbosity=1'])
                except Exception as migrate_error:
                    logger.warning(f"Migration command failed, trying with --run-syncdb: {str(migrate_error)}")
                    try:
                        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=1'])
                    except Exception as sync_error:
                        logger.error(f"Sync migration also failed: {str(sync_error)}")
                        # Don't prevent app startup even if migrations fail
                        pass
                
                self.migrations_run = True
                logger.info("Database migrations completed successfully")
                
            except Exception as e:
                logger.error(f"Migration failed: {str(e)}")
                # Don't block the application if migrations fail
                self.migrations_run = True  # Prevent retry on every request
