# Smart-Customer-Support-Chatbot

An intelligent customer support chatbot built using **Python, Streamlit, Google GenAI API, and Gemini Flash 3.6**.

The chatbot is designed for a fictional e-commerce company called **SmartMart**. It can understand customer queries, detect their intent using a lightweight NLP layer, maintain conversation history, and generate helpful responses using Google's Gemini model.

---

## 📌 Project Overview

Customer support systems receive many repetitive queries related to business hours, orders, delivery, returns, refunds, payments, and complaints.

The **Smart Customer Support Chatbot** provides an interactive conversational interface where users can ask questions in natural language and receive relevant responses.

The application combines:

- Natural Language Processing
- Keyword-based intent detection
- Generative AI
- Conversation history
- Streamlit web application
- Google Gemini API

---

## 🎯 Objectives

The main objectives of this project are:

1. Build an intelligent customer support chatbot.
2. Understand customer queries written in natural language.
3. Detect the possible intent of a customer query.
4. Generate relevant responses using Gemini Flash 3.6.
5. Maintain conversation history for contextual responses.
6. Provide a simple and user-friendly Streamlit interface.
7. Implement API-key security and error handling.
8. Deploy the chatbot as a web application.

---

## ✨ Features

### 💬 Chat Interface

Users can interact with the chatbot through a Streamlit chat interface.

### 🧠 NLP Analysis

The application performs lightweight NLP processing before sending the query to Gemini.

The NLP layer includes:

- Text preprocessing
- Tokenization
- Keyword extraction
- Intent detection
- Confidence estimation

### 🔍 Intent Detection

The chatbot can detect intents such as:

- Greeting
- Goodbye
- Business Hours
- Order Tracking
- Order Status
- Delivery Information
- Return Request
- Refund Request
- Payment Issue
- Cancel Order
- Product Information
- Complaint
- Contact Support

### 🤖 Gemini Flash 3.6

Gemini Flash 3.6 is used to generate natural-language customer support responses.

### 📝 Conversation History

Recent conversation messages are provided to Gemini so that responses can remain contextual.

### 🛡️ API Security

The Gemini API key is loaded through environment variables or Streamlit secrets rather than being hard-coded into the application.

### ⚠️ Error Handling

The application handles situations such as:

- Missing API key
- Invalid API key
- API authentication errors
- Rate limits
- Network errors
- Model availability errors
- Unexpected application errors

### 🏪 SmartMart Support Information

The chatbot is designed around the following fictional SmartMart policies.

#### Business Hours

| Day | Hours |
|---|---|
| Monday – Friday | 9:00 AM – 6:00 PM |
| Saturday | 10:00 AM – 4:00 PM |
| Sunday | Closed |

#### Order Processing

Orders are processed within **1–2 business days**.

#### Delivery

Standard delivery generally takes **3–5 business days** after processing.

#### Returns

Items can be returned within **7 days** if they are:

- Unused
- Undamaged
- In their original packaging

#### Refunds

Refunds are generally processed within **5–7 business days after inspection**.

#### Payment Methods

SmartMart accepts:

- Credit cards
- Debit cards
- UPI
- Net banking

---

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Generative AI:** Google Gemini Flash 3.6
- **API:** Google GenAI API
- **NLP:** Python-based preprocessing and keyword/rule-based intent detection
- **Environment Management:** python-dotenv
- **Data Processing:** Pandas

---

## 📂 Project Structure

```text
smart-customer-support-chatbot/
│
├── app.py
├── chatbot.py
├── nlp_utils.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── AGENTS.md
