"""
nlp_utils.py
------------
Responsible for:
- Text preprocessing (normalization, whitespace cleanup, punctuation handling)
- Keyword extraction
- Intent detection using keyword/rule-based matching

This is a lightweight, educational NLP layer designed to demonstrate
fundamental NLP preprocessing concepts. Gemini 3.6 Flash handles the
actual natural-language understanding and response generation.
"""

import re
import string
from typing import TypedDict

# ---------------------------------------------------------------------------
# Type definition for NLP analysis result
# ---------------------------------------------------------------------------

class NLPAnalysis(TypedDict):
    original_text: str
    preprocessed_text: str
    tokens: list[str]
    keywords: list[str]
    detected_intent: str
    confidence: str


# ---------------------------------------------------------------------------
# Intent definitions with associated keywords
# ---------------------------------------------------------------------------

INTENT_KEYWORDS: dict[str, list[str]] = {
    "greeting": [
        "hello", "hi", "hey", "good morning", "good afternoon",
        "good evening", "howdy", "greetings", "sup", "what's up",
    ],
    "goodbye": [
        "bye", "goodbye", "see you", "take care", "farewell",
        "thanks bye", "thank you bye", "that's all", "thats all",
        "no more questions",
    ],
    "business_hours": [
        "business hours", "opening hours", "working hours", "office hours",
        "open", "closed", "timing", "timings", "when are you open",
        "what time", "hours of operation",
    ],
    "order_tracking": [
        "track", "tracking", "where is my order", "track my order",
        "order status", "shipment", "shipped", "dispatch", "dispatched",
        "out for delivery", "delivery status", "track order",
    ],
    "order_status": [
        "order status", "my order", "order update", "check order",
        "order details", "order number", "order id",
    ],
    "delivery_information": [
        "delivery", "deliver", "home delivery", "shipping", "ship",
        "how long", "how many days", "delivery time", "delivery charge",
        "delivery fee", "free delivery", "express delivery",
    ],
    "return_request": [
        "return", "send back", "give back", "return policy", "how to return",
        "want to return", "return product", "return item", "return process",
    ],
    "refund_request": [
        "refund", "money back", "get my money", "reimbursement",
        "refund policy", "refund status", "when will i get refund",
        "refund process", "how long refund",
    ],
    "payment_issue": [
        "payment failed", "payment not done", "payment issue",
        "payment problem", "transaction failed", "could not pay",
        "payment declined", "card declined", "upi failed",
        "money deducted", "amount deducted", "charged twice",
        "double charged",
    ],
    "cancel_order": [
        "cancel", "cancellation", "cancel my order", "want to cancel",
        "how to cancel", "cancel order", "stop order",
    ],
    "product_information": [
        "product", "item", "details", "specification", "price",
        "availability", "in stock", "out of stock", "product details",
        "warranty", "guarantee",
    ],
    "complaint": [
        "complaint", "issue", "problem", "not working", "broken",
        "damaged", "defective", "wrong item", "wrong product",
        "bad experience", "unhappy", "disappointed", "poor quality",
        "not satisfied", "terrible", "awful", "worst",
    ],
    "contact_support": [
        "contact", "contact support", "speak to agent", "human agent",
        "talk to someone", "customer care", "support team",
        "escalate", "phone number", "email support", "live chat",
        "raise ticket", "support ticket",
    ],
}

# Stop words to filter out from keyword extraction
STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "he", "him", "his",
    "she", "her", "hers", "it", "its", "they", "them", "their",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall",
    "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet",
    "at", "by", "in", "of", "on", "to", "up", "as", "with",
    "about", "into", "through", "during", "before", "after",
    "above", "below", "from", "between", "out", "off", "over",
    "please", "can", "how", "when", "where", "why", "also",
    "just", "really", "very", "quite",
}


# ---------------------------------------------------------------------------
# Text Preprocessing
# ---------------------------------------------------------------------------

def preprocess_text(text: str) -> str:
    """
    Apply lightweight NLP preprocessing to the input text.

    Steps:
    1. Lowercase normalization
    2. Whitespace cleanup (strip + collapse multiple spaces)
    3. Basic punctuation handling (remove most punctuation)

    Returns the cleaned text string.
    """
    if not text:
        return ""

    # Step 1: Lowercase normalization
    text = text.lower()

    # Step 2: Remove punctuation except apostrophes (to preserve contractions)
    punctuation_to_remove = string.punctuation.replace("'", "")
    text = text.translate(str.maketrans("", "", punctuation_to_remove))

    # Step 3: Whitespace cleanup — collapse multiple spaces and strip
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize(text: str) -> list[str]:
    """Split preprocessed text into individual word tokens."""
    return text.split()


def extract_keywords(tokens: list[str]) -> list[str]:
    """
    Extract meaningful keywords by removing stop words.

    Returns a list of content-bearing words.
    """
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 2]


# ---------------------------------------------------------------------------
# Intent Detection
# ---------------------------------------------------------------------------

def detect_intent(preprocessed_text: str) -> tuple[str, str]:
    """
    Detect the user's intent using keyword/rule-based matching.

    Scores each intent by counting how many of its keywords appear
    in the preprocessed text.

    Returns:
        (intent_name, confidence_label)
        confidence_label is one of: "High", "Medium", "Low", "None"
    """
    if not preprocessed_text:
        return "unknown", "None"

    scores: dict[str, int] = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Match whole phrases/words within the text
            if keyword in preprocessed_text:
                # Multi-word phrases get a higher weight
                score += 2 if " " in keyword else 1
        if score > 0:
            scores[intent] = score

    if not scores:
        return "unknown", "None"

    best_intent = max(scores, key=lambda k: scores[k])
    best_score = scores[best_intent]

    # Confidence labeling based on score
    if best_score >= 4:
        confidence = "High"
    elif best_score >= 2:
        confidence = "Medium"
    else:
        confidence = "Low"

    return best_intent, confidence


# ---------------------------------------------------------------------------
# Main NLP Analysis Entry Point
# ---------------------------------------------------------------------------

def analyze_text(user_input: str) -> NLPAnalysis:
    """
    Perform complete NLP analysis on the user's raw input.

    This is the primary function called by the application.

    Args:
        user_input: The raw text entered by the user.

    Returns:
        An NLPAnalysis dict containing:
        - original_text
        - preprocessed_text
        - tokens
        - keywords
        - detected_intent
        - confidence
    """
    original_text = user_input.strip()
    preprocessed_text = preprocess_text(original_text)
    tokens = tokenize(preprocessed_text)
    keywords = extract_keywords(tokens)
    detected_intent, confidence = detect_intent(preprocessed_text)

    return NLPAnalysis(
        original_text=original_text,
        preprocessed_text=preprocessed_text,
        tokens=tokens,
        keywords=keywords,
        detected_intent=detected_intent,
        confidence=confidence,
    )


def format_intent_display(intent: str) -> str:
    """Convert intent snake_case name to a readable display string."""
    return intent.replace("_", " ").title()
