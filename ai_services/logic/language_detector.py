from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def detect_language(text):
    """Detect the language of the input text using AI."""
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Detect the language of the following text. Respond with the language name in English and its ISO 639-1 code.

Text: {text}

Format your response as: "Language Name (ISO Code)"
For example: "English (en)" or "Spanish (es)" or "French (fr)"

If the text contains multiple languages, identify the dominant language."""
    )
    
    llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.1)
    chain = prompt | llm
    
    try:
        result = chain.invoke({"text": text})
        response = result.content.strip()
        
        # Parse the response to extract language and code
        if "(" in response and ")" in response:
            language_part = response.split("(")[0].strip()
            code_part = response.split("(")[1].split(")")[0].strip()
            return {
                "language": language_part,
                "language_code": code_part,
                "raw_response": response,
                "confidence": "high"
            }
        else:
            return {
                "language": response,
                "language_code": "unknown",
                "raw_response": response,
                "confidence": "medium"
            }
    except Exception as e:
        return {"error": f"Language detection failed: {str(e)}"}
