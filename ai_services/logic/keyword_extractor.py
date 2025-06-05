from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser

def extract_keywords(text, count=5):
    """Extract keywords from text using Google's Generative AI."""
    # Use Gemini Pro model instead of text-bison-001
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    
    # Create output parser
    output_parser = CommaSeparatedListOutputParser()
    
    # Create prompt template
    template = """Extract the {count} most important keywords or key phrases from the following text:
    
    TEXT: {text}
    
    Return only the keywords or key phrases as a comma-separated list.
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["text", "count"],
        output_parser=output_parser
    )
    
    # Use modern LangChain pattern (RunnableSequence)
    chain = prompt | llm
    
    # Use invoke instead of run
    try:
        result = chain.invoke({"text": text, "count": count})
        return {"keywords": result}
    except Exception as e:
        # Add more specific error handling
        error_message = str(e)
        if "models/" in error_message and "is not found" in error_message:
            raise ValueError("The AI model is currently unavailable. Please try again later.")
        raise
