from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def answer_question(question, context=None):
    """Answer questions using AI, optionally with provided context."""
    if context:
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""Based on the following context, answer the question as accurately as possible. If the answer cannot be found in the context, say "I cannot find the answer in the provided context."

Context: {context}

Question: {question}

Answer:"""
        )
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
        chain = prompt | llm
        
        try:
            result = chain.invoke({"context": context, "question": question})
            return {
                "answer": result.content.strip(),
                "question": question,
                "has_context": True,
                "context_provided": True
            }
        except Exception as e:
            return {"error": f"Question answering failed: {str(e)}"}
    else:
        prompt = PromptTemplate(
            input_variables=["question"],
            template="""Answer the following question accurately and concisely. Provide factual information when possible.

Question: {question}

Answer:"""
        )
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
        chain = prompt | llm
        
        try:
            result = chain.invoke({"question": question})
            return {
                "answer": result.content.strip(),
                "question": question,
                "has_context": False,
                "context_provided": False
            }
        except Exception as e:
            return {"error": f"Question answering failed: {str(e)}"}
