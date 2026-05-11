import streamlit as st
from groq import Groq
import time
import datetime

st.set_page_config(
    page_title="Neural Interface",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;600&display=swap');

    :root {
        --neon-cyan: #00f5ff;
        --neon-pink: #ff00c8;
        --neon-green: #00ff88;
        --dark-bg: #04050d;
        --card-bg: rgba(0, 20, 35, 0.85);
        --border-glow: rgba(0, 245, 255, 0.4);
    }

    /* ========== ANIMATIONS ========== */
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
        20%, 24%, 55% { opacity: 0.4; }
    }
    @keyframes inputPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(0,245,255,0.3), 0 0 25px rgba(0,245,255,0.1); }
        50%       { box-shadow: 0 0 15px rgba(0,245,255,0.6), 0 0 40px rgba(0,245,255,0.2); }
    }
    @keyframes statusBlink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ========== GLOBAL ========== */
    .stApp {
        background-color: var(--dark-bg);
        background-image:
            radial-gradient(ellipse at 20% 20%, rgba(0, 60, 80, 0.25) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(60, 0, 80, 0.2) 0%, transparent 50%),
            linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
        color: #c8eaf0;
        font-family: 'Share Tech Mono', monospace;
    }

    /* ========== HEADER ========== */
    .hero-container {
        text-align: center;
        padding: 10px 0 20px;
    }
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 8px;
        text-transform: uppercase;
        background: linear-gradient(90deg, var(--neon-cyan), #fff, var(--neon-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: flicker 6s infinite;
        margin: 0;
    }
    .sub-header {
        font-family: 'Share Tech Mono', monospace;
        color: var(--neon-cyan);
        font-size: 0.8rem;
        letter-spacing: 3px;
        margin-top: 6px;
        text-shadow: 0 0 10px var(--neon-cyan);
    }
    .divider-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
        margin: 12px auto;
        width: 60%;
    }

    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060a12 0%, #020508 100%) !important;
        border-right: 1px solid rgba(0,245,255,0.2);
        box-shadow: 4px 0 30px rgba(0, 245, 255, 0.06);
    }
    .sidebar-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--neon-cyan);
        text-align: center;
        letter-spacing: 4px;
        text-shadow: 0 0 14px var(--neon-cyan);
        padding: 10px 0 4px;
    }
    .sidebar-tagline {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.62rem;
        color: rgba(0,245,255,0.4);
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,245,255,0.25), transparent);
        margin: 12px 0;
    }

    /* Status Card */
    .status-card {
        background: rgba(0, 20, 35, 0.8);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    .status-label { font-size: 0.68rem; color: rgba(0,245,255,0.45); letter-spacing: 1px; text-transform: uppercase; }
    .status-value { font-size: 0.72rem; color: var(--neon-green); font-weight: bold; }
    .status-dot {
        display: inline-block; width: 7px; height: 7px; border-radius: 50%;
        background: var(--neon-green); box-shadow: 0 0 8px var(--neon-green);
        margin-right: 5px; animation: statusBlink 1.5s infinite;
    }
    .model-badge {
        background: rgba(0,245,255,0.08); border: 1px solid rgba(0,245,255,0.25);
        border-radius: 4px; padding: 5px 10px; font-size: 0.7rem;
        color: var(--neon-cyan); text-align: center; margin-top: 5px; letter-spacing: 1px;
    }

    /* Session Stats */
    .session-stats { display: flex; gap: 8px; margin-bottom: 12px; }
    .stat-box {
        flex: 1; background: rgba(0,30,45,0.6);
        border: 1px solid rgba(0,245,255,0.15); border-radius: 5px;
        padding: 8px; text-align: center;
    }
    .stat-num { font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: var(--neon-cyan); line-height: 1; }
    .stat-label { font-size: 0.58rem; color: rgba(0,245,255,0.4); letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; }

    /* Chat History Items */
    .history-section-title {
        font-size: 0.62rem;
        color: rgba(0,245,255,0.4);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
        padding-left: 2px;
    }
    .history-item {
        background: rgba(0, 20, 35, 0.6);
        border: 1px solid rgba(0, 245, 255, 0.1);
        border-radius: 5px;
        padding: 8px 12px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.72rem;
        color: rgba(200, 234, 240, 0.7);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .history-item:hover {
        border-color: rgba(0, 245, 255, 0.4);
        background: rgba(0, 30, 50, 0.8);
        color: var(--neon-cyan);
    }
    .history-item.active {
        border-color: var(--neon-cyan);
        background: rgba(0, 50, 70, 0.6);
        color: var(--neon-cyan);
        box-shadow: 0 0 8px rgba(0,245,255,0.15);
    }
    .history-time {
        font-size: 0.58rem;
        color: rgba(0,245,255,0.25);
        margin-top: 2px;
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: transparent !important;
        color: var(--neon-cyan) !important;
        border: 1px solid rgba(0,245,255,0.5) !important;
        border-radius: 4px !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 2px;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        transition: all 0.25s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: rgba(0, 245, 255, 0.12) !important;
        box-shadow: 0 0 14px rgba(0, 245, 255, 0.3);
        transform: translateY(-1px);
    }
    /* Delete/Purge button - pink accent */
    .purge-btn > button {
        color: var(--neon-pink) !important;
        border-color: rgba(255,0,200,0.4) !important;
    }
    .purge-btn > button:hover {
        background: rgba(255, 0, 200, 0.12) !important;
        box-shadow: 0 0 14px rgba(255, 0, 200, 0.3) !important;
    }

    /* ========== CHAT MESSAGES ========== */
    [data-testid="stChatMessage"] {
        background: var(--card-bg) !important;
        border: 1px solid rgba(0, 245, 255, 0.18);
        border-left: 3px solid var(--neon-cyan);
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(6px);
        animation: fadeSlideUp 0.4s ease-out;
        box-shadow: 0 2px 12px rgba(0,0,0,0.4);
    }

    /* ========== CHAT INPUT ========== */
    [data-testid="stChatInputContainer"] {
        background: rgba(0, 8, 18, 0.95) !important;
        border: 1px solid rgba(0, 245, 255, 0.5) !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        animation: inputPulse 3s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        border: none !important;
        color: var(--neon-cyan) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px;
        caret-color: var(--neon-cyan);
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(0, 245, 255, 0.3) !important;
        letter-spacing: 2px;
        font-style: italic;
    }
    [data-testid="stChatInputSubmitButton"] button {
        background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,245,255,0.05)) !important;
        border: 1px solid rgba(0,245,255,0.5) !important;
        border-radius: 6px !important;
        color: var(--neon-cyan) !important;
        transition: all 0.25s ease;
    }
    [data-testid="stChatInputSubmitButton"] button:hover {
        background: var(--neon-cyan) !important;
        color: #000 !important;
        box-shadow: 0 0 20px var(--neon-cyan), 0 0 40px rgba(0,245,255,0.3);
        transform: scale(1.08);
    }
    .input-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.62rem;
        color: rgba(0, 245, 255, 0.35);
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 6px;
        text-transform: uppercase;
    }

    /* ========== ALERTS ========== */
    .stAlert {
        background: rgba(0, 245, 255, 0.07) !important;
        border: 1px solid rgba(0,245,255,0.25) !important;
        border-radius: 4px !important;
        color: var(--neon-cyan) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem !important;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #04050d; }
    ::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.25); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def new_session():
    """Create a new chat session dict."""
    session_id = str(int(time.time()))
    return {
        "id": session_id,
        "title": "New Chat",
        "created_at": datetime.datetime.now().strftime("%H:%M"),
        "messages": [{"role": "assistant", "content": "Connection established. Neural core online. How can I assist you, operator?"}]
    }

if "sessions" not in st.session_state:
    first = new_session()
    st.session_state.sessions = [first]
    st.session_state.active_session_id = first["id"]

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = st.session_state.sessions[0]["id"]

def get_active_session():
    for s in st.session_state.sessions:
        if s["id"] == st.session_state.active_session_id:
            return s
    return st.session_state.sessions[0]

def switch_session(session_id):
    st.session_state.active_session_id = session_id

def delete_session(session_id):
    st.session_state.sessions = [s for s in st.session_state.sessions if s["id"] != session_id]
    if not st.session_state.sessions:
        first = new_session()
        st.session_state.sessions = [first]
        st.session_state.active_session_id = first["id"]
    elif st.session_state.active_session_id == session_id:
        st.session_state.active_session_id = st.session_state.sessions[0]["id"]

# ─── CONFIG ───────────────────────────────────────────────────────────────────
api_key = st.secrets.get("GROQ_API_KEY")
selected_model = "llama-3.1-8b-instant"
active = get_active_session()
msg_count = len([m for m in active["messages"] if m["role"] == "user"])

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">N.I. SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">NEURAL INTERFACE v2.0.0</div>', unsafe_allow_html=True)

    # New Chat button
    if st.button("+ NEW CHAT", use_container_width=True):
        sess = new_session()
        st.session_state.sessions.insert(0, sess)
        st.session_state.active_session_id = sess["id"]
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Connection status
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
        <div class="model-badge">{selected_model}</div>
    </div>
    """, unsafe_allow_html=True)

    # Session stats
    st.markdown(f"""
    <div class="session-stats">
        <div class="stat-box">
            <div class="stat-num">{msg_count}</div>
            <div class="stat-label">Queries</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{len(st.session_state.sessions)}</div>
            <div class="stat-label">Sessions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ── Chat History ──
    st.markdown('<div class="history-section-title">Recent Chats</div>', unsafe_allow_html=True)

    for sess in st.session_state.sessions:
        is_active = sess["id"] == st.session_state.active_session_id
        active_class = "active" if is_active else ""
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="history-item {active_class}" title="{sess['title']}">
                {sess['title'][:30]}{'...' if len(sess['title']) > 30 else ''}
                <div class="history-time">{sess['created_at']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("", key=f"switch_{sess['id']}"):
                switch_session(sess["id"])
                st.rerun()
        with col2:
            if st.button("✕", key=f"del_{sess['id']}"):
                delete_session(sess["id"])
                st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'Share Tech Mono',monospace; font-size:0.58rem; color:rgba(0,245,255,0.2); line-height:1.8;">
        BUILT WITH STREAMLIT &amp; GROQ<br>&copy; 2026 N.I. SYSTEMS
    </div>
    """, unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-container">
    <p class="main-header">Neural Interface</p>
    <div class="divider-line"></div>
    <p class="sub-header">[ {active['title'].upper()} ] &nbsp;|&nbsp; GROQ LPU ENGINE &nbsp;|&nbsp; LLAMA-3.1 CORE</p>
</div>
""", unsafe_allow_html=True)

# ─── CHAT INTERFACE ───────────────────────────────────────────────────────────
active = get_active_session()

for message in active["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('<div class="input-label">// input terminal — type your query below</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Enter command..."):
    if not api_key:
        st.error("ERR_401 // API KEY NOT FOUND IN SECRETS.TOML")
        st.stop()

    active["messages"].append({"role": "user", "content": prompt})

    # Auto-title session from first user message
    if active["title"] == "New Chat":
        active["title"] = prompt[:40]

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            client = Groq(api_key=api_key)
            api_messages = [{"role": m["role"], "content": m["content"]} for m in active["messages"]]
            completion = client.chat.completions.create(
                model=selected_model,
                messages=api_messages,
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "█")
            placeholder.markdown(full_response)
            active["messages"].append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"SYS_ERR // {e}")
