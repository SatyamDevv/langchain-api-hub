from django.apps import AppConfig


class AiServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_services'
    
    def ready(self):
        """Initialize LangChain models when Django starts to prevent Pydantic errors in production."""
        try:
            # Import and initialize LangChain models
            from .logic.langchain_init import get_initialized_llm
            # This will trigger the model rebuild and cache initialization
            get_initialized_llm()
        except Exception as e:
            # Log the error but don't prevent the app from starting
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to pre-initialize LangChain models: {str(e)}")
            pass
