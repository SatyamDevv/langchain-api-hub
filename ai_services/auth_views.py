from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction, connection
import json
import logging
from django.conf import settings
from .models import APIKey
from .db_utils import safe_database_operation

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_protect
def login_view(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Test database connection before authentication
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except Exception as db_error:
                logger.error(f"Database connection failed during login: {str(db_error)}")
                messages.error(request, 'Database connection issue. Please try again in a moment.')
                return render(request, 'ai_services/login.html')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Create API key if it doesn't exist with database transaction
                try:
                    with transaction.atomic():
                        api_key, created = APIKey.objects.get_or_create(user=user)
                        if created:
                            logger.info(f"Created new API key for user {username}")
                        else:
                            logger.info(f"Using existing API key for user {username}")
                    
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                    
                except Exception as e:
                    # Log the specific error but don't fail the login
                    logger.error(f"API key creation error for user {username}: {str(e)}")
                    
                    # Try without transaction as fallback
                    try:
                        api_key, created = APIKey.objects.get_or_create(user=user)
                        messages.success(request, 'Login successful!')
                        return redirect('home')
                    except Exception as e2:
                        logger.error(f"API key fallback creation failed for user {username}: {str(e2)}")
                        # Still log the user in even if API key creation fails
                        messages.warning(request, 'Login successful, but there was an issue with your API key. Please contact support.')
                        return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                
        except Exception as e:
            # Log the detailed error with more context
            error_msg = str(e)
            logger.error(f"Login error for user {username}: {error_msg}")
            
            # Check if it's a database connection error
            if any(keyword in error_msg.lower() for keyword in [
                'connection', 'timeout', 'network', 'cannot assign', 'host', 'server'
            ]):
                messages.error(request, 'Database connection issue. Please try again in a moment.')
            elif settings.DEBUG:
                messages.error(request, f'Login error: {error_msg}')
            else:
                messages.error(request, 'An error occurred during login. Please try again.')
    
    return render(request, 'ai_services/login.html')

@csrf_protect
def signup_view(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'ai_services/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'ai_services/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'ai_services/signup.html')
          # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create API key
            api_key = APIKey.objects.create(user=user)
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred while creating your account: {str(e)}')
            return render(request, 'ai_services/signup.html')
    
    return render(request, 'ai_services/signup.html')

@login_required
def dashboard_view(request):
    try:
        api_key = APIKey.objects.get(user=request.user)
    except APIKey.DoesNotExist:
        try:
            api_key = APIKey.objects.create(user=request.user)
        except Exception as e:
            messages.error(request, 'Unable to create API key. Please contact support.')
            api_key = None
    except Exception as e:
        messages.error(request, 'Unable to retrieve API key. Please contact support.')
        api_key = None
    
    return render(request, 'ai_services/dashboard.html', {
        'api_key': api_key,
        'user': request.user
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
@require_http_methods(["POST"])
def regenerate_api_key(request):
    try:
        api_key = APIKey.objects.get(user=request.user)
        api_key.key = APIKey.generate_api_key()
        api_key.usage_count = 0
        api_key.save()
        
        return JsonResponse({
            'success': True,
            'new_key': api_key.key,
            'message': 'API key regenerated successfully!'
        })
    except APIKey.DoesNotExist:
        api_key = APIKey.objects.create(user=request.user)
        return JsonResponse({
            'success': True,
            'new_key': api_key.key,
            'message': 'API key created successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })
