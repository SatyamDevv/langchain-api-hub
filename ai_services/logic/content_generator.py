from langchain_core.prompts import PromptTemplate
from .langchain_init import get_initialized_llm

def generate_content(prompt_text, content_type="general", max_length=500):
    """Generate creative content based on the prompt and content type."""
    
    content_templates = {
        "email": """Write a professional email based on the following requirements:

{prompt_text}

Make it professional, clear, and concise. Include appropriate greeting and closing.""",
        
        "story": """Write a creative story based on the following prompt:

{prompt_text}

Make it engaging and imaginative. Keep it around {max_length} words.""",
        
        "blog": """Write a blog post based on the following topic:

{prompt_text}

Make it informative, engaging, and well-structured. Include an introduction, main points, and conclusion.""",
        
        "social_media": """Create a social media post based on the following idea:

{prompt_text}

Make it engaging, concise, and suitable for social media platforms. Include relevant hashtags if appropriate.""",
        
        "product_description": """Write a compelling product description based on the following details:

{prompt_text}

Highlight key features, benefits, and make it appealing to potential customers.""",
        
        "general": """Generate content based on the following prompt:

{prompt_text}

Be creative and provide useful, well-written content."""
    }
    
    template = content_templates.get(content_type, content_templates["general"])
    
    prompt = PromptTemplate(
        input_variables=["prompt_text", "max_length"],
        template=template
    )
    
    llm = get_initialized_llm(model="gemini-2.0-flash", temperature=0.7)
    chain = prompt | llm
    
    try:
        result = chain.invoke({"prompt_text": prompt_text, "max_length": max_length})
        return {
            "generated_content": result.content.strip(),
            "content_type": content_type,
            "original_prompt": prompt_text,
            "max_length": max_length,
            "word_count": len(result.content.strip().split())
        }
    except Exception as e:
        return {"error": f"Content generation failed: {str(e)}"}
