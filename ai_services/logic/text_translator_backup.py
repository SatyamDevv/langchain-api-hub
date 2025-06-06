from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def translate_text(text, target_language, source_language="auto"):
    """Translate text from source language to target language using AI."""
    if source_language == "auto":
        prompt = PromptTemplate(
            input_variables=["text", "target_language"],
            template="""Translate the following text to {target_language}. Maintain the original meaning and tone.

Text to translate: {text}

Provide only the translation without any additional explanation."""
        )
        
        llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.1)
        result = prompt | llm
        
        try:
            translation = result.invoke({"text": text, "target_language": target_language})
            return {
                "translated_text": translation.content.strip(),
                "source_language": "auto-detected",
                "target_language": target_language,
                "original_text": text
            }
        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}
    else:
        prompt = PromptTemplate(
            input_variables=["text", "source_language", "target_language"],
            template="""Translate the following text from {source_language} to {target_language}. Maintain the original meaning and tone.

Text to translate: {text}

Provide only the translation without any additional explanation."""
        )
          llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.1)
        result = prompt | llm
        
        try:
            translation = result.invoke({
                "text": text, 
                "source_language": source_language,
                "target_language": target_language
            })
            return {
                "translated_text": translation.content.strip(),
                "source_language": source_language,
                "target_language": target_language,
                "original_text": text
            }
        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}
