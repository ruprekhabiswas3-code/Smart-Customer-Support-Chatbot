"""
chatbot.py
----------
Responsible for:
- Gemini API initialization
- Building system instructions
- Sending messages with conversation history to Gemini
- Receiving and returning responses
- Error handling for API and network issues
"""

import google.genai as genai
from google.genai import types
from google.auth.credentials import Credentials
from google.oauth2.credentials import Credentials as OAuth2Credentials

from config import (
    get_api_key,
    is_api_key_configured,
    GEMINI_MODEL,
    SYSTEM_INSTRUCTION,
    MAX_HISTORY_TURNS,
)


# ---------------------------------------------------------------------------
# Gemini Client Initialization
# ---------------------------------------------------------------------------

def get_gemini_client() -> genai.Client | None:
    """
    Create and return a configured Gemini API client.

    Supports both:
    - Standard API keys (AIzaSy...) via api_key parameter
    - Auth tokens (AQ...) via google.oauth2 credentials

    Returns None if the API key is not configured.
    """
    if not is_api_key_configured():
        return None

    api_key = get_api_key().strip()
    try:
        # Auth token format (AQ. prefix) — use OAuth2 credentials
        if api_key.startswith("AQ.") or api_key.startswith("ya29."):
            creds = OAuth2Credentials(token=api_key)
            client = genai.Client(credentials=creds)
        else:
            # Standard API key (AIzaSy...)
            client = genai.Client(api_key=api_key)
        return client
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Response Generation
# ---------------------------------------------------------------------------

def build_contents(
    conversation_history: list[dict],
    user_message: str,
) -> list[types.Content]:
    """
    Convert the stored conversation history and the new user message
    into the format expected by the Google GenAI SDK.

    Args:
        conversation_history: List of dicts with keys "role" and "content".
                              Roles are "user" or "assistant".
        user_message: The latest user message string.

    Returns:
        A list of types.Content objects ready to send to Gemini.
    """
    contents: list[types.Content] = []

    # Include recent history (limit to MAX_HISTORY_TURNS turns = pairs)
    # Each turn = one user + one assistant message
    recent_history = conversation_history[-(MAX_HISTORY_TURNS * 2):]

    for msg in recent_history:
        # Map "assistant" role to "model" (required by Gemini API)
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])],
            )
        )

    # Add the new user message
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)],
        )
    )

    return contents


def generate_response(
    conversation_history: list[dict],
    user_message: str,
) -> tuple[str, str | None]:
    """
    Send the user message (with conversation history) to Gemini
    and return the generated response.

    Args:
        conversation_history: Previous messages as a list of
                               {"role": str, "content": str} dicts.
        user_message: The latest message from the user.

    Returns:
        A tuple (response_text, error_message).
        On success: (response_text, None)
        On failure: ("", error_description)
    """
    # Validate API key
    if not is_api_key_configured():
        return (
            "",
            "⚠️ Gemini API key is not configured. "
            "Please add **GEMINI_API_KEY** to your `.env` file "
            "or Streamlit secrets and restart the application.",
        )

    # Validate user input
    user_message = user_message.strip()
    if not user_message:
        return "", "Empty message. Please type a question."

    # Build client
    client = get_gemini_client()
    if client is None:
        return (
            "",
            "⚠️ Failed to initialize the Gemini API client. "
            "Please check your API key and try again.",
        )

    # Build conversation contents
    contents = build_contents(conversation_history, user_message)

    # Configure generation settings
    generation_config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.7,
        max_output_tokens=1024,
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=generation_config,
        )

        # Extract the text from the response
        if response and response.text:
            return response.text.strip(), None

        # Handle empty/blocked response
        return (
            "",
            "⚠️ The assistant could not generate a response. "
            "Please rephrase your question and try again.",
        )

    except Exception as exc:
        error_str = str(exc).lower()

        if "api_key" in error_str or "api key" in error_str or "invalid" in error_str or "unauthorized" in error_str:
            return "", "⚠️ Invalid or unauthorized API key. Please verify your **GEMINI_API_KEY** is correct."
        elif "quota" in error_str or "rate" in error_str or "limit" in error_str:
            return "", "⚠️ API rate limit or quota exceeded. Please wait a moment and try again."
        elif "network" in error_str or "connection" in error_str or "timeout" in error_str:
            return "", "⚠️ Network error. Please check your internet connection and try again."
        elif "not_found" in error_str or "404" in error_str:
            return "", "⚠️ The AI model is currently unavailable. Please try again in a moment."
        else:
            return "", "⚠️ An unexpected error occurred while contacting the assistant. Please try again in a moment."


# ---------------------------------------------------------------------------
# API Key Validation Helper
# ---------------------------------------------------------------------------

def validate_api_key() -> tuple[bool, str]:
    """
    Attempt a minimal API call to verify that the API key is valid.

    Returns:
        (is_valid: bool, message: str)
    """
    if not is_api_key_configured():
        return (
            False,
            "API key is not configured. Add GEMINI_API_KEY to your .env file.",
        )

    client = get_gemini_client()
    if client is None:
        return False, "Failed to create Gemini client."

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part(text="Hello")],
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are a test assistant. Reply with: OK",
                max_output_tokens=10,
            ),
        )
        if response and response.text:
            return True, "API key is valid."
        return False, "Received an empty response during validation."
    except Exception as exc:
        return False, f"Validation failed: {type(exc).__name__}"
