from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import APIKey
import json
import warnings
import os

# Suppress the specific static files warning
warnings.filterwarnings('ignore', message='No directory at: /var/task/staticfiles_build/static/')

class APIKeyAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate API requests using API keys
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Try to create static directory if it doesn't exist (for deployment environments)
        static_dir = '/var/task/staticfiles_build/static/'
        if not os.path.exists(static_dir) and os.access(os.path.dirname(static_dir), os.W_OK):
            try:
                os.makedirs(static_dir, exist_ok=True)
            except (OSError, PermissionError):
                # Just log the error but don't fail initialization
                pass
    
    def process_request(self, request):
        # List of endpoints that require API key authentication
        api_endpoints = [
            '/summarize/',
            '/sentiment/',
            '/keywords/',
            '/classify/',
            '/detect-language/',
            '/translate/',
            '/answer/',
            '/generate/',
            # Also handle API routes with prefix
            '/api/services/summarize/',
            '/api/services/sentiment/',
            '/api/services/keywords/',
            '/api/services/classify/',
            '/api/services/detect-language/',
            '/api/services/translate/',
            '/api/services/answer/',
            '/api/services/generate/'
        ]
        
        # Check if the request is for an API endpoint
        if any(request.path.startswith(endpoint) for endpoint in api_endpoints):
            # Get API key from header
            api_key = request.META.get('HTTP_X_API_KEY')
            
            if not api_key:
                # Try to get from request body if it's a POST request
                if request.method == 'POST':
                    try:
                        body = json.loads(request.body.decode('utf-8'))
                        api_key = body.get('api_key')
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass
            
            if not api_key:
                return JsonResponse({
                    'error': 'API key required',
                    'message': 'Please provide a valid API key in the X-API-Key header or request body'
                }, status=401)
            
            # Validate API key
            try:
                api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
                # Increment usage count
                api_key_obj.usage_count += 1
                api_key_obj.save()
                
                # Add user to request for use in views
                request.api_user = api_key_obj.user
                
            except APIKey.DoesNotExist:
                return JsonResponse({
                    'error': 'Invalid API key',
                    'message': 'The provided API key is not valid or has been deactivated'
                }, status=401)
        
        return None
