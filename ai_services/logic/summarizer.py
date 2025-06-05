from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def summarize_text(text, method="stuff"):
    # Initialize the LLM directly
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", model_kwargs={})
    
    # Create a simple summarization prompt
    prompt_template = """Please provide a concise summary of the following text:

{text}

Summary:"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    
    # Generate summary directly
    response = llm.invoke(prompt.format(text=text))
    
    return response.content
