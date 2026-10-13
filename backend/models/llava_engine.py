
import os

from dotenv import load_dotenv
from google import genai

# Load backend/.env
load_dotenv()

API_KEY = os.getenv("gemini_api_key")
MODEL_NAME = "gemini-3.8-flash"


def run_llava(
    image_path: str,
    prompt: str,
    source_code: str = "",
) -> str:
    """
    Gemini-powered debugging assistant.
    The function name is retained for compatibility with app.py.
    """
    if not API_KEY:
        return (
            "Configuration Error:\n"
            "GEMINI_API_KEY was not found. Check backend/.env."
        )

    debugging_input = (
        f"Debugging instructions:\n{prompt}\n\n"
        f"Submitted source code:\n{source_code or 'No source code provided.'}"
    )

    try:
        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=debugging_input,
        )

        if not response.text:
            return "Gemini returned an empty response. Please try again."

        return (
            "Analysis Mode: Gemini LLM\n\n"
            + response.text
        )

    except Exception as exc:
        print(f"Gemini API error: {exc}")
        return (
            "Gemini API Error:\n"
            f"{type(exc).__name__}: {exc}"
        )

