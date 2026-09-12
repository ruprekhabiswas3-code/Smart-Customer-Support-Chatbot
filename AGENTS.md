# AGENTS.md — Project Development Instructions

This file defines the development rules and guidelines for the
**Smart Customer Support Chatbot** project.
These instructions must be followed by any developer (human or AI agent)
contributing to this codebase.

---

## 📐 Architecture Rules

- **Python only.** Do not introduce Node.js, Java, Go, or any other backend language.
- **Streamlit only for UI.** Do not use Flask, Django, FastAPI, React, or any other web framework.
- **Keep the architecture flat and simple.** The project has exactly four Python source files:
  - `app.py` — Streamlit UI
  - `chatbot.py` — Gemini API integration
  - `nlp_utils.py` — NLP preprocessing and intent detection
  - `config.py` — Configuration and constants
- Do not add new Python source files unless absolutely necessary and clearly justified.
- Do not introduce databases, background task queues, or cloud services beyond the Gemini API.

---

## 🤖 LLM / Gemini API Rules

- **Use `gemini-3.6-flash` as the model.** Do not change this without updating all references.
- **Use the `google-genai` Python SDK** (import as `google.genai`).
  Do not use `google-generativeai` or any other Gemini SDK variant.
- **Always use `client.models.generate_content()`** with `types.Content` and `types.Part`.
- **Always pass the system instruction via `types.GenerateContentConfig(system_instruction=...)`.**
- Do not hardcode the API key anywhere in the source code.
- Read the API key using `config.get_api_key()`, which checks Streamlit secrets first,
  then environment variables / `.env`.

---

## 🔑 API Key & Security Rules

- **Never** place a real API key in any `.py`, `.toml`, `.json`, or `.yaml` file.
- **Never** commit `.env` to Git. It is listed in `.gitignore`.
- `.env.example` is the only key-related file that may be committed.
  It must contain only the placeholder: `GEMINI_API_KEY=your_api_key_here`
- Do not modify the structure of `.env.example` unless the key name changes.
- The application must work with both local `.env` and Streamlit Cloud secrets
  without code changes.

---

## 🧠 NLP Layer Rules

- Keep intent detection in `nlp_utils.py` as keyword/rule-based.
  Do not introduce `scikit-learn`, `spaCy`, `NLTK`, or any ML framework
  unless explicitly requested.
- NLP analysis must be computed before calling Gemini and must be stored
  alongside the message in `st.session_state.nlp_analyses`.
- The NLP Analysis expander is educational — keep it accurate and readable.
- If new intents are added, add them to both `INTENT_KEYWORDS` in `nlp_utils.py`
  and document them in `README.md`.

---

## 💬 Conversation History Rules

- All messages are stored in `st.session_state.messages` as a list of
  `{"role": str, "content": str}` dicts. Roles are `"user"` or `"assistant"`.
- When calling `generate_response()`, pass all history **except** the current
  user message as `conversation_history`. The current message is passed separately.
- The history passed to Gemini is limited to `MAX_HISTORY_TURNS` (10) turn pairs
  to avoid exceeding token limits. Adjust in `config.py` if needed.
- Never wipe `st.session_state.messages` except through the "Clear Chat" or
  "New Chat" buttons.

---

## 🎨 Streamlit UI Rules

- Use `st.chat_message()` and `st.chat_input()` for the chat interface.
- Use `st.spinner()` while waiting for Gemini responses.
- Use `st.error()` for error messages — never expose raw exception text to users.
- Keep custom CSS minimal. Do not add animations, gradients, or heavy styling.
- `st.set_page_config()` must always be the first Streamlit call in `app.py`.
- Do not use `st.experimental_rerun()` — use `st.rerun()` instead.

---

## ⚙️ Code Quality Rules

- Use clear, descriptive variable and function names.
- Every function must have a docstring.
- Add type hints to all function signatures.
- Do not leave `TODO`, `FIXME`, `HACK`, or `pass` stubs in production code.
- Do not create placeholder/fake functions that return hardcoded responses.
- Handle all foreseeable errors gracefully and display user-friendly messages.
- Do not swallow exceptions silently — at minimum log the error type.

---

## 📦 Dependency Rules

- `requirements.txt` must list only the packages actually used:
  `streamlit`, `google-genai`, `python-dotenv`, `pandas`.
- Do not pin versions unless a specific version is required to fix a bug.
- Do not introduce optional or heavy dependencies (e.g., `torch`, `transformers`).

---

## 🚀 Deployment Compatibility Rules

- The application must run with `streamlit run app.py` with no additional arguments.
- All configuration must be read from environment variables or Streamlit secrets.
- Do not use `subprocess`, `os.system`, or shell commands in application code.
- Do not write files to disk at runtime (logs, caches, temp files).

---

## ✅ Pre-Commit Checklist

Before committing changes:

- [ ] All Python files pass `python -m py_compile <file>.py` with no errors.
- [ ] `streamlit run app.py` starts without errors.
- [ ] The API key is not hardcoded anywhere.
- [ ] `.env` is not staged for commit.
- [ ] All new functions have docstrings and type hints.
- [ ] `requirements.txt` reflects actual dependencies.
- [ ] `README.md` is up to date.

---

## 🧪 Testing Guidelines

Run the following manual tests after every significant change:

1. Start the app: `streamlit run app.py`
2. Verify the welcome message and suggested questions appear.
3. Test at least: greeting, business hours, delivery, return, refund,
   payment issue, order tracking, complaint, unknown topic.
4. Verify the NLP Analysis expander shows correct intent and keywords.
5. Verify conversation history carries context across follow-up questions.
6. Test with API key removed to verify the error message appears.
7. Verify Clear Chat and New Chat buttons work correctly.
