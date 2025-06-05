"""
Supabase utility functions for Django integration
"""
import os
import logging
from django.db import connection
from django.core.management.color import no_style
from django.db.backends.utils import CursorWrapper

logger = logging.getLogger(__name__)

def test_supabase_connection():
    """Test the Supabase database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            logger.info(f"Successfully connected to PostgreSQL: {result[0]}")
            return True
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        return False

def get_supabase_connection_info():
    """Get current database connection information"""
    try:
        with connection.cursor() as cursor:
            # Get current database info
            cursor.execute("""
                SELECT 
                    current_database() as db_name,
                    current_user as user_name,
                    inet_server_addr() as server_ip,
                    inet_server_port() as server_port,
                    version() as pg_version
            """)
            result = cursor.fetchone()
            
            connection_info = {
                'database': result[0],
                'user': result[1], 
                'server_ip': result[2],
                'server_port': result[3],
                'version': result[4]
            }
            
            logger.info(f"Database connection info: {connection_info}")
            return connection_info
            
    except Exception as e:
        logger.error(f"Failed to get connection info: {str(e)}")
        return None

def check_supabase_pooler():
    """Check if we're using connection pooler"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW server_version;")
            result = cursor.fetchone()
            
            # Check if we're connected through pooler
            with connection.cursor() as cursor:
                cursor.execute("SELECT inet_server_port();")
                port = cursor.fetchone()[0]
                
            is_pooler = port == 6543
            logger.info(f"Connection port: {port}, Using pooler: {is_pooler}")
            return is_pooler
            
    except Exception as e:
        logger.error(f"Failed to check pooler status: {str(e)}")
        return False

def optimize_supabase_settings():
    """Apply Supabase-specific optimizations"""
    optimizations = {
        'CONN_MAX_AGE': 60,  # Short-lived for serverless
        'CONN_HEALTH_CHECKS': True,
        'AUTOCOMMIT': True,
    }
    
    logger.info("Applied Supabase optimizations")
    return optimizations
