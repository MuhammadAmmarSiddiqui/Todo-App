from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Create OpenAI client configured for Gemini API
# The OpenAI client supports custom base URLs, allowing us to use Gemini's OpenAI-compatible endpoint
gemini_client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    max_retries=0, # Disable automatic retries to save quota
)
