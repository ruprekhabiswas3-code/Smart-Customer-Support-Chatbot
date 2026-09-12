"""
config.py
---------
Responsible for:
- Loading environment variables from .env (local) or Streamlit secrets (cloud)
- Validating the Gemini API key
- Providing configuration constants for the application
"""

import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# ---------------------------------------------------------------------------
# API Key Loading
# ---------------------------------------------------------------------------

def get_api_key() -> str | None:
    """
    Returns the Gemini API key.

    Priority:
    1. Streamlit secrets (used on Streamlit Community Cloud)
    2. Environment variable / .env file (used for local development)
    """
    # Try Streamlit secrets first (only available when running inside Streamlit)
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        if api_key:
            return api_key
    except Exception:
        pass

    # Fall back to environment variable (loaded from .env via python-dotenv)
    return os.getenv("GEMINI_API_KEY")


def is_api_key_configured() -> bool:
    """Returns True if a non-empty API key is available."""
    key = get_api_key()
    return bool(key and key.strip())


# ---------------------------------------------------------------------------
# SmartMart Business Information
# (FICTIONAL sample data for demonstration purposes only)
# ---------------------------------------------------------------------------

COMPANY_NAME = "SmartMart"

BUSINESS_INFO = """
SMARTMART BUSINESS INFORMATION (FICTIONAL - FOR DEMONSTRATION PURPOSES ONLY)
===========================================================================

Company Name: SmartMart

Business Hours:
  Monday–Friday : 9:00 AM – 6:00 PM
  Saturday      : 10:00 AM – 4:00 PM
  Sunday        : Closed

Order Processing:
  Orders are normally processed within 1–2 business days after payment confirmation.

Delivery:
  Standard delivery normally takes 3–5 business days after dispatch.
  Home delivery is available to eligible pin codes.

Return Policy:
  Products can normally be returned within 7 days of delivery,
  provided they are unused, undamaged, and in original packaging.

Refund Policy:
  Eligible refunds are normally processed within 5–7 business days
  after the returned product has been received and inspected.

Payment Methods Accepted:
  Credit card, debit card, UPI, and net banking.

Customer Support:
  Customers can contact SmartMart customer support through this chatbot.
  For complex issues, a support ticket can be raised and a human agent will follow up.

Damaged / Defective Products:
  If you received a damaged or defective product, please contact support
  immediately with your order ID and photos of the damage.
  A replacement or refund will be arranged after verification.

Order Cancellation:
  Orders can typically be cancelled before they are dispatched.
  Once dispatched, cancellation may not be possible.

DISCLAIMER:
  SmartMart is a fictional company created solely for educational and
  demonstration purposes. All information above is sample/fictional data.
"""

# ---------------------------------------------------------------------------
# Gemini Model Configuration
# ---------------------------------------------------------------------------

GEMINI_MODEL = "gemini-3.6-flash"

# Maximum number of past conversation turns to include in context
MAX_HISTORY_TURNS = 10

# ---------------------------------------------------------------------------
# System Instruction for Gemini
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = f"""
You are a professional, polite, and helpful customer support assistant for SmartMart.

SmartMart is a fictional retail company used for demonstration purposes.

Use the following SmartMart business information to answer customer questions accurately:

{BUSINESS_INFO}

RULES YOU MUST FOLLOW:
1. Be polite, professional, and concise in all responses.
2. Answer only based on the SmartMart business information provided above.
3. Do NOT invent company policies that are not listed above.
4. Do NOT claim to have accessed any order database or real system.
5. Do NOT claim that an order has actually been shipped, cancelled, or refunded.
   Instead, explain the policy and advise the customer on the steps to follow.
6. If specific order information is needed, ask the customer for their Order ID.
7. Do NOT ask for passwords, card numbers, CVV numbers, OTPs, or any sensitive credentials.
8. If a question is too complex or cannot be resolved through the chatbot,
   politely ask the customer to raise a support ticket and inform them a human agent will follow up.
9. If the customer asks something unrelated to SmartMart customer support,
   politely explain that you are designed primarily for SmartMart customer support
   and redirect the conversation.
10. Keep answers concise and easy to understand. Avoid unnecessarily long responses.
11. Use conversation history to understand follow-up questions in context.
12. Always be empathetic when the customer has a complaint or issue.
"""

# ---------------------------------------------------------------------------
# UI Constants
# ---------------------------------------------------------------------------

APP_TITLE = "Smart Customer Support Chatbot"
APP_ICON = "🤖"
APP_SUBTITLE = "An NLP + Generative AI customer support assistant powered by Gemini 3.6 Flash"
TECH_STACK = "Python | NLP | Gemini 3.6 Flash | Streamlit"

SUGGESTED_QUESTIONS = [
    "How can I track my order?",
    "What is your return policy?",
    "What payment methods do you accept?",
    "How long does delivery take?",
    "How can I cancel my order?",
    "What are your business hours?",
]
