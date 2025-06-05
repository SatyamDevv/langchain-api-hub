"""
Database utilities for handling connection issues in production
"""
import logging
import time
from django.db import connection
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

def test_database_connection(max_retries=3, retry_delay=1):
    """
    Test database connection with retry logic
    """
    for attempt in range(max_retries):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    logger.info(f"Database connection successful on attempt {attempt + 1}")
                    return True, "Connection successful"
        except OperationalError as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed: {error_msg}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error(f"Database connection failed after {max_retries} attempts: {error_msg}")
                return False, error_msg
        except Exception as e:
            error_msg = f"Database connection failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    return False, "Unknown database error"

def safe_database_operation(operation, *args, **kwargs):
    """
    Safely execute a database operation with error handling and retries
    """
    max_retries = kwargs.pop('max_retries', 2)
    
    for attempt in range(max_retries):
        try:
            # Test connection first
            is_connected, error_msg = test_database_connection(max_retries=1)
            if not is_connected:
                if attempt < max_retries - 1:
                    logger.warning(f"Database not connected, retrying operation in 1s...")
                    time.sleep(1)
                    continue
                else:
                    logger.error(f"Cannot execute operation: {error_msg}")
                    return None
            
            # Execute the operation
            return operation(*args, **kwargs)
            
        except OperationalError as e:
            if "cannot assign requested address" in str(e).lower():
                logger.error(f"IPv6/Network connectivity issue: {str(e)}")
            elif attempt < max_retries - 1:
                logger.warning(f"Database operation failed on attempt {attempt + 1}: {str(e)}. Retrying...")
                time.sleep(1)
            else:
                logger.error(f"Database operation failed after {max_retries} attempts: {str(e)}")
            
        except Exception as e:
            logger.error(f"Database operation failed: {str(e)}")
            return None
    
    return None

def check_database_health():
    """
    Comprehensive database health check with detailed error reporting
    """
    health_status = {
        'connected': False,
        'tables_exist': False,
        'migrations_applied': False,
        'error': None,
        'connection_details': {}
    }
    
    try:
        # Get connection details
        db_config = connection.settings_dict
        health_status['connection_details'] = {
            'engine': db_config.get('ENGINE', 'Unknown'),
            'host': db_config.get('HOST', 'Unknown'),
            'port': db_config.get('PORT', 'Unknown'),
            'name': db_config.get('NAME', 'Unknown'),
        }
        
        # Test connection with retries
        is_connected, error_msg = test_database_connection(max_retries=3)
        health_status['connected'] = is_connected
        
        if not is_connected:
            health_status['error'] = error_msg
            # Add specific guidance for common errors
            if "cannot assign requested address" in error_msg.lower():
                health_status['error'] += " (IPv6/Network connectivity issue - check Vercel network settings)"
            elif "timeout" in error_msg.lower():
                health_status['error'] += " (Connection timeout - check firewall/network settings)"
            elif "authentication failed" in error_msg.lower():
                health_status['error'] += " (Check database credentials)"
            return health_status
        
        # Check if tables exist
        table_names = connection.introspection.table_names()
        health_status['tables_exist'] = len(table_names) > 0
        
        # Check if Django tables exist (basic migration check)
        django_tables = ['django_migrations', 'auth_user']
        has_django_tables = any(table in table_names for table in django_tables)
        health_status['migrations_applied'] = has_django_tables
        
    except Exception as e:
        health_status['error'] = str(e)
        logger.error(f"Database health check failed: {str(e)}")
    
    return health_status
