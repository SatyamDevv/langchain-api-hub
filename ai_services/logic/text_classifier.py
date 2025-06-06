from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def classify_text(text, categories=None):
    """Classify text into predefined categories using AI."""
    if categories is None:
        categories = ["Technology", "Business", "Sports", "Entertainment", "Politics", "Science", "Health", "Education", "Travel", "Food"]
    
    categories_str = ", ".join(categories)
    
    prompt = PromptTemplate(
        input_variables=["text", "categories"],
        template="""Classify the following text into one of these categories: {categories}

Text: {text}

Respond with only the category name that best fits the text content. Choose the most appropriate category from the list provided."""
    )
    
    llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.1)
    chain = prompt | llm
    
    try:
        result = chain.invoke({"text": text, "categories": categories_str})
        category = result.content.strip()
        
        # Ensure the returned category is in our list (case-insensitive)
        for cat in categories:
            if cat.lower() == category.lower():
                return {"category": cat, "confidence": "high", "available_categories": categories}
        
        return {"category": category, "confidence": "medium", "available_categories": categories}
    except Exception as e:
        return {"error": f"Classification failed: {str(e)}"}
