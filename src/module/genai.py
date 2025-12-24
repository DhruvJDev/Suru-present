import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Create client with API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def llm_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

# Test
if __name__ == "__main__":
    print(llm_response("How to start a startup company?"))
