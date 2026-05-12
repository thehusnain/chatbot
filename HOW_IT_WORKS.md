# How This Chatbot Was Built — Step by Step
### Subject: Artificial Intelligence | Author: Husnain

---

## What is this project?

This is a **ChatGPT-style AI Chatbot** that runs in your browser.  
It is built using three tools:

| Tool | What it does |
|------|-------------|
| **Python** | The programming language everything is written in |
| **Streamlit** | Turns Python code into a beautiful web app (no HTML needed) |
| **Groq API** | The AI brain — gives us access to the Llama 3 language model |

---

## Project Folder Structure

```
groq_chatbot_dashboard/
│
├── app.py              ← The main Python file (the brain of the app)
├── style.css           ← All the visual styling (colors, fonts, animations)
├── requirements.txt    ← List of Python libraries to install
│
├── .streamlit/
│   └── secrets.toml   ← Your private API key (never pushed to GitHub)
│
├── .gitignore          ← Tells Git what NOT to upload
│
└── husnain/            ← Virtual Environment (your isolated Python space)
```

---

## Step 1 — Virtual Environment (husnain/)

A virtual environment is like a private room for your project.
It keeps libraries installed only for this project.

```bash
# Create it
python3 -m venv husnain

# Activate it (run this every time you open a terminal)
source husnain/bin/activate

# Install libraries inside it
pip install streamlit groq
```

---

## Step 2 — The API Key (.streamlit/secrets.toml)

An API key is like a password that lets your app talk to the Groq AI service.
You get it for free from console.groq.com.

Store it in `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-api-key-here"
```

The app reads it securely like this:
```python
api_key = st.secrets.get("GROQ_API_KEY")
```

Never put the key directly in app.py — it would be visible on GitHub.

---

## Step 3 — requirements.txt

A simple text file listing the libraries needed:
```
streamlit
groq
```

Anyone can install them with:
```bash
pip install -r requirements.txt
```

---

## Step 4 — style.css (The Visual Design)

CSS controls how things look — colors, fonts, animations.
We separated it from app.py so the code stays readable.

In app.py, we load it like this:
```python
def load_css(filepath):
    with open(filepath) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")
```

Key design choices in style.css:

| Feature | What it does |
|---------|-------------|
| @import url(...) | Loads Orbitron and Share Tech Mono fonts from Google |
| :root { --neon-cyan } | Color variables — change colors from one place |
| @keyframes flicker | Makes the title flicker like a neon sign |
| @keyframes inputPulse | Makes the text box glow rhythmically |
| .stApp background | Draws a dark grid pattern as the background |
| stChatMessage | Styles each chat bubble with a glowing cyan border |

---

## Step 5 — app.py Explained

### Imports
```python
import streamlit as st   # The web framework
from groq import Groq    # The AI API client
import time              # For generating unique IDs
import datetime          # For showing timestamps
```

### Session Dictionary
Every conversation is stored as a dictionary:
```python
{
    "id": "1715492000",    # Unique number (timestamp)
    "title": "New Chat",   # Shown in sidebar
    "created_at": "09:30", # Creation time
    "messages": [...]      # All messages in this chat
}
```

### st.session_state — Streamlit's Memory
Streamlit reruns the page on every button click.
session_state survives those reruns — it's the app's memory.

```python
st.session_state.sessions  = [session1, session2, ...]
st.session_state.active_id = "1715492000"
```

### Displaying Messages
```python
for message in active["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

### The AI Call (Streaming)
```python
completion = client.chat.completions.create(
    model=MODEL,
    messages=api_messages,
    stream=True,   # ← This sends words one by one (typing effect)
)
```

---

## Step 6 — Running the App

```bash
source husnain/bin/activate
streamlit run app.py
```

Browser opens at: http://localhost:8501

---

## Step 7 — Deploying Online (Streamlit Cloud)

1. Push code to GitHub (secrets.toml stays local, it is in .gitignore)
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Add your GROQ_API_KEY in the Streamlit Cloud Secrets section
5. Click Deploy — you get a free public URL

---

## Summary Diagram

```
You type a message
        |
        v
  app.py receives it
        |
        v
  Sent to Groq API (with full chat history)
        |
        v
  Groq AI (Llama 3) generates a reply
        |
        v
  Streamed back word-by-word to browser
        |
        v
  Saved into session_state for history
```

---

Built with Python, Streamlit and Groq — by Husnain
