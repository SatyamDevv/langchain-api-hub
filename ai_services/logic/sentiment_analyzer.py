from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def analyze_sentiment(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Analyze the sentiment of the following text. Respond only with one of: 'positive', 'negative', or 'neutral'.\nText: {text}"
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", model_kwargs={})
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"sentiment": result.content.strip()}
