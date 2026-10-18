
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load the .env file located beside this test script.
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check backend/.env."
    )

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: Gemini connection successful."
    )

    print("Model:", model)
    print("Response:", response.text or "(No text returned)")
    print("Gemini API test completed.")

except Exception as exc:
    # Do not print credentials or environment variables.
    print("Gemini API request failed.")
    print("Error type:", type(exc).__name__)
    print("Check your API key, model access, quota, and internet connection.")
    raise
