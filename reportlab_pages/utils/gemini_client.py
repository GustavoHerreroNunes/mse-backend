import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.oauth2 import service_account

load_dotenv()

_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./msesolucoes-1739d0a595ea.json")
_PROJECT = os.getenv("VERTEX_AI_PROJECT", "msesolucoes")
_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

try:
    _credentials = service_account.Credentials.from_service_account_file(
        _KEY_PATH, scopes=_SCOPES
    )
    _client = genai.Client(
        vertexai=True,
        project=_PROJECT,
        location=_LOCATION,
        credentials=_credentials,
    )
except Exception as exc:
    logging.error(f"Failed to initialize Gemini client: {exc}")
    _client = None


def prompt_model(system: str, user: str, max_tokens: int) -> str:
    """
    Send a prompt to the Gemini model on Vertex AI and return the text response.

    Args:
        system: System instruction for the model.
        user: User message / prompt content.
        max_tokens: Maximum number of output tokens.

    Returns:
        The model's text response.
    """
    if _client is None:
        raise RuntimeError("Gemini client is not initialized.")

    response = _client.models.generate_content(
        model=_MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=0,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text
