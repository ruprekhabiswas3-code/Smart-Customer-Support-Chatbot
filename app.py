"""
app.py
------
Responsible for:
- Streamlit page configuration and layout
- Chat interface (messages, input)
- Sidebar (about, topics, controls)
- Session state management (conversation history)
- Suggested question buttons
- NLP analysis expandable section
- Displaying responses from chatbot.py
- Error and loading state handling
"""

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    APP_SUBTITLE,
    TECH_STACK,
    COMPANY_NAME,
    SUGGESTED_QUESTIONS,
    is_api_key_configured,
)
from chatbot import generate_response
from nlp_utils import analyze_text, format_intent_display

# ---------------------------------------------------------------------------
# Page Configuration  (must be the very first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — minimal, professional styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* Header area */
    .main-header {
        text-align: center;
        padding: 0.5rem 0 1rem 0;
    }
    .main-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #57606a;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .tech-stack {
        color: #3b82d4;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Suggested question chips */
    .suggested-label {
        color: #57606a;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }

    /* NLP analysis box */
    .nlp-table td { padding: 2px 8px; font-size: 0.88rem; }
    .nlp-table tr:first-child td { font-weight: 600; }

    /* Status badge */
    .status-ok  { color: #2da44e; font-weight: 600; }
    .status-err { color: #cf222e; font-weight: 600; }

    /* Sidebar footer */
    .sidebar-footer {
        font-size: 0.75rem;
        color: #57606a;
        margin-top: 1rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------

def init_session_state() -> None:
    """Initialise all session-state keys if not already present."""
    if "messages" not in st.session_state:
        st.session_state.messages = []          # list of {role, content}
    if "nlp_analyses" not in st.session_state:
        st.session_state.nlp_analyses = []      # parallel list of NLPAnalysis
    if "conversation_count" not in st.session_state:
        st.session_state.conversation_count = 1
    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None   # holds a suggested-question click


init_session_state()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.markdown("---")

    # About section
    st.markdown("### ℹ️ About")
    st.markdown(
        f"""
        This chatbot is an **NLP + Generative AI** project that demonstrates
        how a rule-based NLP preprocessing layer combines with
        **Gemini 3.6 Flash** to deliver intelligent customer support responses
        for the fictional company **{COMPANY_NAME}**.

        > ⚠️ *SmartMart is a fictional company created solely for
        educational/demonstration purposes.*
        """
    )

    st.markdown("---")

    # How to use
    st.markdown("### 📖 How to Use")
    st.markdown(
        """
        1. Type your question in the chat box below.
        2. Press **Enter** or click **Send**.
        3. The assistant will reply based on SmartMart policies.
        4. Expand **NLP Analysis** under each message to see
           the detected intent and extracted keywords.
        """
    )

    st.markdown("---")

    # Supported topics
    st.markdown("### 📋 Supported Topics")
    topics = [
        "🕐 Business hours",
        "📦 Order tracking & status",
        "🚚 Delivery information",
        "↩️ Returns & refunds",
        "💳 Payment methods & issues",
        "❌ Order cancellation",
        "🛍️ Product information",
        "📣 Complaints",
        "📞 Contact support",
    ]
    for topic in topics:
        st.markdown(f"- {topic}")

    st.markdown("---")

    # API key status
    st.markdown("### 🔑 API Status")
    if is_api_key_configured():
        st.markdown('<span class="status-ok">✅ Gemini API key configured</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-err">❌ API key not configured</span>', unsafe_allow_html=True)
        st.warning(
            "Add `GEMINI_API_KEY` to your `.env` file or Streamlit secrets.",
            icon="⚠️",
        )

    st.markdown("---")

    # Conversation controls
    st.markdown("### 🛠️ Controls")
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.nlp_analyses = []
            st.rerun()

    with col_b:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.nlp_analyses = []
            st.session_state.conversation_count += 1
            st.rerun()

    st.markdown(
        '<div class="sidebar-footer">Conversation #'
        f'{st.session_state.conversation_count}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Header
# ---------------------------------------------------------------------------

st.markdown(
    f"""
    <div class="main-header">
        <h1>{APP_ICON} {APP_TITLE}</h1>
        <p class="subtitle">{APP_SUBTITLE}</p>
        <p class="tech-stack">Technologies: {TECH_STACK}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Show API key warning banner in main area too (if missing)
if not is_api_key_configured():
    st.error(
        "**Gemini API key is not configured.**  \n"
        "Please add `GEMINI_API_KEY=your_api_key_here` to your `.env` file "
        "and restart the application.  \n"
        "Refer to the README for setup instructions.",
        icon="🔑",
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Welcome message (shown only when history is empty)
# ---------------------------------------------------------------------------

if not st.session_state.messages:
    st.info(
        f"👋 Welcome! I'm the **{COMPANY_NAME}** virtual support assistant.  \n"
        "I can help you with orders, deliveries, returns, refunds, and more.  \n"
        "Type your question below or choose one of the suggested topics.",
        icon="🤖",
    )

# ---------------------------------------------------------------------------
# Suggested Questions
# ---------------------------------------------------------------------------

st.markdown('<p class="suggested-label">💡 Suggested questions:</p>', unsafe_allow_html=True)

# Render suggested-question buttons in rows of 3
cols_per_row = 3
for row_start in range(0, len(SUGGESTED_QUESTIONS), cols_per_row):
    row_questions = SUGGESTED_QUESTIONS[row_start : row_start + cols_per_row]
    cols = st.columns(len(row_questions))
    for col, question in zip(cols, row_questions):
        with col:
            if st.button(question, key=f"sq_{question}", use_container_width=True):
                st.session_state.pending_input = question

st.markdown("")

# ---------------------------------------------------------------------------
# Render existing conversation history
# ---------------------------------------------------------------------------

# Build a lookup: index of user messages → index into nlp_analyses
user_msg_indices = [i for i, m in enumerate(st.session_state.messages) if m["role"] == "user"]
nlp_lookup = {
    msg_idx: nlp_idx
    for nlp_idx, msg_idx in enumerate(user_msg_indices)
}

for msg_idx, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]

    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        st.markdown(content)

        # Show NLP analysis under each user message
        if role == "user":
            nlp_idx = nlp_lookup.get(msg_idx)
            if nlp_idx is not None and nlp_idx < len(st.session_state.nlp_analyses):
                analysis = st.session_state.nlp_analyses[nlp_idx]
                with st.expander("🔍 NLP Analysis", expanded=False):
                    kw_display = ", ".join(analysis["keywords"]) if analysis["keywords"] else "—"
                    st.markdown(
                        f"""
                        | Field | Value |
                        |---|---|
                        | **Detected Intent** | `{format_intent_display(analysis["detected_intent"])}` |
                        | **Confidence** | {analysis["confidence"]} |
                        | **Keywords Extracted** | {kw_display} |
                        | **Preprocessed Text** | *{analysis["preprocessed_text"]}* |
                        """
                    )

# ---------------------------------------------------------------------------
# Process a pending suggested-question click
# ---------------------------------------------------------------------------

def handle_user_input(user_text: str) -> None:
    """
    Process a user message: run NLP analysis, call Gemini, update history.
    This function is called for both typed input and suggested-question clicks.
    """
    user_text = user_text.strip()
    if not user_text:
        return

    # 1. NLP analysis
    analysis = analyze_text(user_text)

    # 2. Store user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.nlp_analyses.append(analysis)

    # 3. Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_text)
        with st.expander("🔍 NLP Analysis", expanded=False):
            kw_display = ", ".join(analysis["keywords"]) if analysis["keywords"] else "—"
            st.markdown(
                f"""
                | Field | Value |
                |---|---|
                | **Detected Intent** | `{format_intent_display(analysis["detected_intent"])}` |
                | **Confidence** | {analysis["confidence"]} |
                | **Keywords Extracted** | {kw_display} |
                | **Preprocessed Text** | *{analysis["preprocessed_text"]}* |
                """
            )

    # 4. Generate and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        # Show spinner while Gemini generates the response
        with st.spinner("SmartMart assistant is thinking…"):
            # Pass all history EXCEPT the message we just appended
            # (the current message is passed separately as user_message)
            history_for_api = st.session_state.messages[:-1]
            response_text, error_msg = generate_response(history_for_api, user_text)

        if error_msg:
            st.error(error_msg)
            # Store a placeholder so history stays consistent
            st.session_state.messages.append(
                {"role": "assistant", "content": f"[Error] {error_msg}"}
            )
        else:
            st.markdown(response_text)
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )


# Handle pending click from a suggested-question button
if st.session_state.pending_input:
    pending = st.session_state.pending_input
    st.session_state.pending_input = None
    handle_user_input(pending)

# ---------------------------------------------------------------------------
# Chat Input  (pinned to the bottom of the page by Streamlit)
# ---------------------------------------------------------------------------

user_input = st.chat_input(
    placeholder="Ask your question about SmartMart…",
    key="chat_input",
)

if user_input:
    handle_user_input(user_input)
