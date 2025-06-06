from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def analyze_sentiment(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Analyze the sentiment of the following text. Respond only with one of: 'positive', 'negative', or 'neutral'.\nText: {text}"
    )
    llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.0)
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"sentiment": result.content.strip()}
