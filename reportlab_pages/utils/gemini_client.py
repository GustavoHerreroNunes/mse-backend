import os
import json
import logging
from dotenv import load_dotenvk
from google import genai
from google.genai import types
from google.oauth2 import service_account

load_dotenv()


# We now fetch the raw string instead of a path
_CREDS_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
_PROJECT = os.getenv("VERTEX_AI_PROJECT", "msesolucoes")
_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

_client = None

try:
    if not _CREDS_JSON:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON not found in environment variables.")

    # Parse the JSON string into a dictionary
    info = json.loads(_CREDS_JSON)
    
    # Initialize credentials from the dictionary
    _credentials = service_account.Credentials.from_service_account_info(
        info, scopes=_SCOPES
    )
    
    _client = genai.Client(
        vertexai=True,
        project=_PROJECT,
        location=_LOCATION,
        credentials=_credentials,
    )
except Exception as exc:
    logging.error(f"Failed to initialize Gemini client: {exc}")


def prompt_model(system: str, user: str, max_tokens: int) -> str:
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