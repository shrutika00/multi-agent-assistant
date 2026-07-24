import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from backend directory or parent directories
load_dotenv()

# Check for API key
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def generate_text(prompt: str, system_instruction: str = None) -> str:
    """
    Calls the Gemini API to generate content with an optional system instruction.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to your backend/.env file.")
        
    genai.configure(api_key=key)
    model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    
    # Initialize the generative model
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
    )
    
    try:
        response = model.generate_content(prompt)
        if not response.text:
            raise Exception("Received empty response from Gemini API.")
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")
