
import os
from google import genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Select Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"


def get_llm_response(question, context):

    prompt = f"""
    You are a helpful AI assistant.

    Answer the question using ONLY the provided context.

    Context:
    {context}

    Question:
    {question}

    If the answer is not available in the context,
    say "I don't have enough information."
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
