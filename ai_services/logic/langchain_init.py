"""
LangChain initialization module to fix Pydantic model issues in production.
This module ensures proper initialization of LangChain models for serverless deployments.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize and rebuild models to fix Pydantic issues
try:
    # Force model rebuild to resolve Pydantic initialization issues
    ChatGoogleGenerativeAI.model_rebuild()
except Exception as e:
    # Ignore rebuild errors in case they're already built
    pass

def get_initialized_llm(model="gemini-2.0-flash", temperature=0.0, **kwargs):
    """
    Get a properly initialized ChatGoogleGenerativeAI instance.
    This function ensures the model is properly configured for production environments.
    """
    # Ensure API key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    # Create the LLM instance with proper initialization
    try:
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=api_key,
            **kwargs
        )
        return llm
    except Exception as e:
        # Fallback: try rebuilding the model again
        try:
            ChatGoogleGenerativeAI.model_rebuild()
            llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                google_api_key=api_key,
                **kwargs
            )
            return llm
        except Exception as rebuild_error:
            raise Exception(f"Failed to initialize ChatGoogleGenerativeAI: {str(e)}. Rebuild attempt also failed: {str(rebuild_error)}")
