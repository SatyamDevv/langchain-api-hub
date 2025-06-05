from django.urls import path
from .views import (
    SummarizationView, SentimentAnalysisView, KeywordExtractionView, HomeView,
    TextClassificationView, LanguageDetectionView, TextTranslationView,
    QuestionAnsweringView, ContentGenerationView, health_check, db_info
)
from .auth_views import (
    login_view, signup_view, logout_view, regenerate_api_key
)

urlpatterns = [
     path("", HomeView.as_view(), name="home"),
    path("dashboard/", HomeView.as_view(), name="dashboard"),
    path("health/", health_check, name="health_check"),
    path("db-info/", db_info, name="db_info"),
    
    # Authentication URLs
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("regenerate-api-key/", regenerate_api_key, name="regenerate_api_key"),
    
    # API endpoints
    path("summarize/", SummarizationView.as_view(), name="summarize"),
    path("sentiment/", SentimentAnalysisView.as_view(), name="sentiment"),
    path("keywords/", KeywordExtractionView.as_view(), name="keywords"),
    path("classify/", TextClassificationView.as_view(), name="classify"),
    path("detect-language/", LanguageDetectionView.as_view(), name="detect_language"),
    path("translate/", TextTranslationView.as_view(), name="translate"),
    path("answer/", QuestionAnsweringView.as_view(), name="answer"),
    path("generate/", ContentGenerationView.as_view(), name="generate"),
]
