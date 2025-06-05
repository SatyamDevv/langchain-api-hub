from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views import View
from django.middleware.csrf import get_token
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import logging
from .db_utils import check_database_health

from ai_services.logic.keyword_extractor import extract_keywords
from ai_services.logic.text_classifier import classify_text
from ai_services.logic.language_detector import detect_language
from ai_services.logic.text_translator import translate_text
from ai_services.logic.question_answerer import answer_question
from ai_services.logic.content_generator import generate_content
from .models import APIKey
from .serializers import (
    KeywordRequestSerializer, SentimentRequestSerializer, SummarizationSerializer,
    TextClassificationSerializer, LanguageDetectionSerializer, TextTranslationSerializer,
    QuestionAnsweringSerializer, ContentGenerationSerializer
)
from .logic.summarizer import summarize_text
from .logic.sentiment_analyzer import analyze_sentiment

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    health = check_database_health()
    
    status_code = 200 if health['connected'] else 503
    
    return JsonResponse({
        'status': 'healthy' if health['connected'] else 'unhealthy',
        'database': health,
        'timestamp': timezone.now().isoformat()
    }, status=status_code)

@require_http_methods(["GET"])
def db_info(request):
    """Get detailed database connection information (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            # Get connection info
            cursor.execute("""
                SELECT 
                    current_database() as db_name,
                    current_user as user_name,
                    inet_server_addr() as server_ip,
                    inet_server_port() as server_port
            """)
            result = cursor.fetchone()
            
            # Check if using pooler
            is_pooler = result[3] == 6543
            
            return JsonResponse({
                'database_name': result[0],
                'user': result[1],
                'server_ip': result[2],
                'server_port': result[3],
                'using_pooler': is_pooler,
                'connection_type': 'pooler' if is_pooler else 'direct'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class HomeView(View):
    def get(self, request):
        # Get CSRF token
        csrf_token = get_token(request)
        # Get API key if user is authenticated
        api_key = None
        if request.user.is_authenticated:
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
            'csrf_token': csrf_token,
            'api_key': api_key,
            'user': request.user
        })

class SummarizationView(APIView):
    def post(self, request):
        serializer = SummarizationSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]
            method = serializer.validated_data["method"]
            try:
                summary = summarize_text(text, method)
                return Response({"summary": summary}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SentimentAnalysisView(APIView):
    def post(self, request):
        serializer = SentimentRequestSerializer(data=request.data)
        if serializer.is_valid():
            result = analyze_sentiment(serializer.validated_data["text"])
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class KeywordExtractionView(APIView):
    def post(self, request):
        serializer = KeywordRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = extract_keywords(serializer.validated_data["text"], serializer.validated_data["count"])
                return Response(result, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during keyword extraction"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextClassificationView(APIView):
    def post(self, request):
        serializer = TextClassificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                text = serializer.validated_data["text"]
                categories = serializer.validated_data.get("categories", None)
                result = classify_text(text, categories)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during text classification"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageDetectionView(APIView):
    def post(self, request):
        serializer = LanguageDetectionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = detect_language(serializer.validated_data["text"])
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during language detection"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextTranslationView(APIView):
    def post(self, request):
        serializer = TextTranslationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                text = serializer.validated_data["text"]
                target_language = serializer.validated_data["target_language"]
                source_language = serializer.validated_data.get("source_language", "auto")
                result = translate_text(text, target_language, source_language)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during translation"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionAnsweringView(APIView):
    def post(self, request):
        serializer = QuestionAnsweringSerializer(data=request.data)
        if serializer.is_valid():
            try:
                question = serializer.validated_data["question"]
                context = serializer.validated_data.get("context", None)
                result = answer_question(question, context)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during question answering"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentGenerationView(APIView):
    def post(self, request):
        serializer = ContentGenerationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prompt_text = serializer.validated_data["prompt_text"]
                content_type = serializer.validated_data.get("content_type", "general")
                max_length = serializer.validated_data.get("max_length", 500)
                result = generate_content(prompt_text, content_type, max_length)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred during content generation"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
