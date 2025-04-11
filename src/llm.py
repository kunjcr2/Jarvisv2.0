import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm(api_key):
    '''
    LLM
    '''
    # api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    try:
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
        )
        return llm
    except Exception as e:
        print(f"Error initializing ChatOpenAI: {str(e)}")
        raise
