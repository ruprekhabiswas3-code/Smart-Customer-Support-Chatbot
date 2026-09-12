# 🤖 Smart Customer Support Chatbot

> **An NLP + Generative AI customer support assistant powered by Gemini 2.5 Flash**

---

## 📌 Project Description

**Smart Customer Support Chatbot** is a student-level web application that demonstrates
how lightweight **Natural Language Processing (NLP)** preprocessing can be combined with
a **Large Language Model (LLM)** — specifically Google Gemini 2.5 Flash — to build an
intelligent, context-aware customer support chatbot.

The chatbot represents **SmartMart**, a *fictional* retail company created solely for
educational and demonstration purposes. It can answer questions about business hours,
order tracking, delivery, returns, refunds, payment methods, and more.

---

## ✨ Features

- 💬 Interactive chat interface built with Streamlit
- 🧠 Gemini 2.5 Flash for natural-language response generation
- 🔍 NLP Analysis panel (intent detection, keyword extraction)
- 📜 Conversation history with context-aware follow-up understanding
- 💡 Suggested quick-action question buttons
- 🗑️ Clear Chat and New Conversation controls
- ⚠️ Robust error handling (missing key, invalid key, network errors, rate limits)
- ⏳ Spinner/loading indicator while the LLM generates a response
- 🔒 API key never hardcoded — loaded from `.env` or Streamlit secrets
- ☁️ Compatible with Streamlit Community Cloud deployment

---

## 🧪 NLP Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Lowercase normalization | `text.lower()` in `nlp_utils.py` |
| Whitespace cleanup | `re.sub(r"\s+", " ", text).strip()` |
| Punctuation handling | `str.translate(str.maketrans(...))` |
| Tokenization | `text.split()` |
| Stop-word removal | Predefined stop-word set |
| Keyword extraction | Tokens minus stop words |
| Intent detection | Keyword/rule-based scoring |

> The application does **not** train a machine-learning model.
> Rule-based intent detection is used for educational clarity.
> Gemini 2.5 Flash handles full natural-language understanding.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI framework | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| LLM SDK | `google-genai` |
| Environment variables | `python-dotenv` |
| Data utility | `pandas` |

---

## 🗂️ Project Architecture

```
smart-customer-support-chatbot/
│
├── app.py            ← Streamlit UI, chat interface, session state
├── chatbot.py        ← Gemini API integration, response generation
├── nlp_utils.py      ← Text preprocessing, keyword extraction, intent detection
├── config.py         ← API key loading, configuration constants, system instruction
├── requirements.txt  ← Python dependencies
├── .env.example      ← API key template (safe to commit)
├── .gitignore        ← Files excluded from Git
├── README.md         ← This file
└── AGENTS.md         ← Development guidelines
```

---

## 💼 Sample Business Information

> ⚠️ **All SmartMart information below is FICTIONAL, created for demonstration purposes only.**

| Topic | Details |
|---|---|
| Company | SmartMart |
| Business Hours | Mon–Fri 9 AM–6 PM, Sat 10 AM–4 PM, Sun Closed |
| Order Processing | 1–2 business days |
| Standard Delivery | 3–5 business days |
| Return Window | 7 days from delivery (unused, original condition) |
| Refund Processing | 5–7 business days after inspection |
| Payment Methods | Credit card, debit card, UPI, net banking |

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or newer
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- `pip` package manager

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/smart-customer-support-chatbot.git
cd smart-customer-support-chatbot
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

```bash
# Copy the example file
cp .env.example .env          # macOS/Linux
copy .env.example .env        # Windows

# Open .env in any text editor and replace the placeholder:
# GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application locally

```bash
streamlit run app.py
```

The application opens at **http://localhost:8501** in your default browser.

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Create a GitHub repository** and push the project files.
   - Make sure `.env` is listed in `.gitignore` — do NOT push it.

2. **Open** [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in.

3. Click **New app** → select your GitHub repository.

4. Set **Main file path** to `app.py`.

5. Open **Advanced settings → Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your_actual_api_key"
   ```

6. Click **Deploy**.

The application reads the API key from Streamlit secrets automatically when running on the cloud.

---

## 💬 Example Questions to Test

| Category | Example question |
|---|---|
| Greeting | "Hello!" |
| Business hours | "What are your business hours?" |
| Order tracking | "How can I track my order?" |
| Delivery | "How long does delivery take?" |
| Returns | "How can I return a product?" |
| Refund | "What is your refund policy?" |
| Payment issue | "My payment failed. What should I do?" |
| Cancel order | "How can I cancel my order?" |
| Complaint | "I received a damaged product." |
| Contact | "How can I contact customer support?" |
| Unknown | "What is the capital of France?" |

---

## 🧪 Test Plan

| # | Test | Expected behaviour |
|---|---|---|
| 1 | Type "Hello" | Friendly greeting response |
| 2 | Ask about business hours | Correct Mon–Sun hours |
| 3 | Ask about delivery time | "3–5 business days" |
| 4 | Ask about returns | 7-day return window policy |
| 5 | Ask about refunds | 5–7 business day refund policy |
| 6 | Describe payment failure | Troubleshooting guidance |
| 7 | Ask how to track order | Order tracking guidance + Order ID request |
| 8 | Report damaged product | Empathetic response + next steps |
| 9 | Ask unrelated question | Polite redirect to SmartMart topics |
| 10 | Press Enter with empty input | No crash, input ignored |
| 11 | Missing API key | Clear error message in UI |

---

## 🔒 Security Notes

- **Never** place your actual API key in any source file.
- **Never** commit `.env` to Git — it is listed in `.gitignore`.
- The `.env.example` file contains only a placeholder and is safe to commit.
- For Streamlit Cloud, use the built-in **Secrets** manager.
- The chatbot will never ask users for passwords, card numbers, OTPs, or CVV codes.

---

## 🔮 Future Enhancements

- Connect to a real order management database for live order lookup
- Add multi-language support
- Add voice input/output using the Web Speech API
- Integrate feedback mechanism (thumbs up / thumbs down per response)
- Add user authentication for personalised order queries
- Use a fine-tuned model for domain-specific accuracy
- Add analytics dashboard for common customer intents

---

## 📄 Disclaimer

SmartMart is a **fictional company** created solely for educational and demonstration
purposes. All business information (hours, policies, prices) is sample/fictional data
and does not represent any real business.
