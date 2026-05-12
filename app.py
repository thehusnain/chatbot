# ============================================================
#  app.py — Neural Interface Chatbot
#  Built with: Python, Streamlit, Groq API
#  Author: Husnain
# ============================================================

# ── Step 1: Import required libraries ───────────────────────
import streamlit as st   # The web framework that builds our UI
from groq import Groq    # The AI API client
import time              # For generating unique session IDs
import datetime          # For showing chat timestamps


# ── Step 2: Configure the browser tab ───────────────────────
st.set_page_config(
    page_title="Neural Interface",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ── Step 3: Load CSS from separate file ─────────────────────
# We keep all styling in style.css to keep this file clean
def load_css(filepath):
    with open(filepath) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")


# ── Step 4: Load the API key from secrets.toml ──────────────
# Streamlit reads .streamlit/secrets.toml automatically
api_key = st.secrets.get("GROQ_API_KEY")

# The AI model we want to use (free and fast)
MODEL = "llama-3.1-8b-instant"


# ── Step 5: Multi-session chat logic ────────────────────────
# Each "session" is one conversation. We store all sessions
# in st.session_state so they survive page reruns.

def create_new_session():
    """Creates a blank new chat session (like pressing New Chat in ChatGPT)."""
    return {
        "id": str(int(time.time())),                           # Unique ID using timestamp
        "title": "New Chat",                                   # Title shown in sidebar
        "created_at": datetime.datetime.now().strftime("%H:%M"),  # Time stamp
        "messages": [                                          # Starting message from AI
            {"role": "assistant", "content": "Connection established. Neural core online. How can I assist you, operator?"}
        ]
    }

def get_active_session():
    """Returns the currently selected chat session."""
    for session in st.session_state.sessions:
        if session["id"] == st.session_state.active_id:
            return session
    return st.session_state.sessions[0]  # fallback to first if not found

def switch_to_session(session_id):
    """Switches the view to a different chat session."""
    st.session_state.active_id = session_id

def delete_session(session_id):
    """Deletes a chat session. If it was active, switches to the first remaining one."""
    st.session_state.sessions = [s for s in st.session_state.sessions if s["id"] != session_id]
    # If no sessions remain, create a fresh one
    if not st.session_state.sessions:
        new = create_new_session()
        st.session_state.sessions = [new]
        st.session_state.active_id = new["id"]
    # If deleted session was the active one, switch to the first
    elif st.session_state.active_id == session_id:
        st.session_state.active_id = st.session_state.sessions[0]["id"]


# ── Step 6: First-time initialization ───────────────────────
# Only runs once when the app first loads
if "sessions" not in st.session_state:
    first_session = create_new_session()
    st.session_state.sessions = [first_session]
    st.session_state.active_id = first_session["id"]


# ── Step 7: Build the Sidebar ───────────────────────────────
active = get_active_session()
user_msg_count = len([m for m in active["messages"] if m["role"] == "user"])

with st.sidebar:
    # Title
    st.markdown('<div class="sidebar-logo">N.I. SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">NEURAL INTERFACE v2.0.0</div>', unsafe_allow_html=True)

    # New Chat button
    if st.button("+ NEW CHAT", use_container_width=True):
        new = create_new_session()
        st.session_state.sessions.insert(0, new)
        st.session_state.active_id = new["id"]
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Connection / Model status card
    st.markdown(f"""
    <div class="status-card">
        <div class="status-row">
            <span class="status-label">Status</span>
            <span class="status-value"><span class="status-dot"></span>ONLINE</span>
        </div>
        <div class="status-row">
            <span class="status-label">Core</span>
            <span class="status-value" style="color:#00f5ff;">GROQ LPU</span>
        </div>
        <div class="model-badge">{MODEL}</div>
    </div>
    """, unsafe_allow_html=True)

    # Live stats: queries sent & total sessions open
    st.markdown(f"""
    <div class="session-stats">
        <div class="stat-box">
            <div class="stat-num">{user_msg_count}</div>
            <div class="stat-label">Queries</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{len(st.session_state.sessions)}</div>
            <div class="stat-label">Sessions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Chat History list
    st.markdown('<div class="history-section-title">Recent Chats</div>', unsafe_allow_html=True)

    for session in st.session_state.sessions:
        is_active = session["id"] == st.session_state.active_id
        active_class = "active" if is_active else ""

        col_title, col_delete = st.columns([5, 1])
        with col_title:
            # Show session title — truncated if too long
            st.markdown(f"""
            <div class="history-item {active_class}">
                {session['title'][:30]}{'...' if len(session['title']) > 30 else ''}
                <div class="history-time">{session['created_at']}</div>
            </div>
            """, unsafe_allow_html=True)
            # Invisible button on top of the history item to handle click
            if st.button(" ", key=f"switch_{session['id']}"):
                switch_to_session(session["id"])
                st.rerun()
        with col_delete:
            if st.button("✕", key=f"del_{session['id']}"):
                delete_session(session["id"])
                st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-size:0.58rem; color:rgba(0,245,255,0.2); line-height:1.8;">
        BUILT WITH STREAMLIT &amp; GROQ<br>&copy; 2026 HUSNAIN
    </div>
    """, unsafe_allow_html=True)


# ── Step 8: Page Header ─────────────────────────────────────
active = get_active_session()  # re-fetch in case session switched

st.markdown(f"""
<div class="hero-container">
    <p class="main-header">Neural Interface</p>
    <div class="divider-line"></div>
    <p class="sub-header">[ {active['title'].upper()} ] &nbsp;|&nbsp; GROQ LPU ENGINE &nbsp;|&nbsp; LLAMA-3.1 CORE</p>
</div>
""", unsafe_allow_html=True)


# ── Step 9: Display Chat Messages ───────────────────────────
# Loop through the active session's messages and show each one
for message in active["messages"]:
    with st.chat_message(message["role"]):   # "user" or "assistant"
        st.markdown(message["content"])


# ── Step 10: Handle New User Input ──────────────────────────
st.markdown('<div class="input-label">// input terminal — type your query below</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Enter command..."):

    # Guard: make sure the API key exists
    if not api_key:
        st.error("ERR_401 // API KEY NOT FOUND IN .streamlit/secrets.toml")
        st.stop()

    # Save the user's message into the active session
    active["messages"].append({"role": "user", "content": prompt})

    # Auto-set session title from the first message the user sends
    if active["title"] == "New Chat":
        active["title"] = prompt[:40]

    # Show the user's message immediately on screen
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the Groq API and stream the response back
    with st.chat_message("assistant"):
        placeholder = st.empty()      # A blank area we will fill with streamed text
        full_response = ""

        try:
            client = Groq(api_key=api_key)

            # Send the entire conversation history so the AI has context
            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in active["messages"]
            ]

            # stream=True means we get the response word-by-word (faster feel)
            completion = client.chat.completions.create(
                model=MODEL,
                messages=api_messages,
                stream=True,
            )

            # Build up the response text as each word arrives
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "█")  # █ = typing cursor

            # Display the final clean response (no cursor)
            placeholder.markdown(full_response)

            # Save the AI's response into the session history
            active["messages"].append({"role": "assistant", "content": full_response})

            # Rerun the page so the sidebar stats update
            st.rerun()

        except Exception as e:
            st.error(f"SYS_ERR // {e}")
