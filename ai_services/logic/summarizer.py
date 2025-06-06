from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def summarize_text(text, method="stuff"):
    # Initialize the LLM using the centralized function
    llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.0)
    
    # Create a simple summarization prompt
    prompt_template = """Please provide a concise summary of the following text:

{text}

Summary:"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    
    # Generate summary directly
    response = llm.invoke(prompt.format(text=text))
    
    return response.content
