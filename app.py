import streamlit as st
from groq import Groq
import time

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

    /* ========== ANIMATIONS ========== */
    @keyframes glitch {
        0%   { clip-path: inset(0 0 95% 0); transform: skewX(-5deg); }
        10%  { clip-path: inset(80% 0 0 0);  transform: skewX(3deg);  }
        20%  { clip-path: inset(40% 0 50% 0); transform: skewX(-2deg); }
        100% { clip-path: inset(0 0 100% 0); transform: skewX(0); }
    }
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
        20%, 24%, 55% { opacity: 0.4; }
    }
    @keyframes scanline {
        0%   { top: -10%; }
        100% { top: 110%; }
    }
    @keyframes inputPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(0,245,255,0.3), 0 0 25px rgba(0,245,255,0.1), inset 0 0 10px rgba(0,245,255,0.03); }
        50%       { box-shadow: 0 0 15px rgba(0,245,255,0.6), 0 0 40px rgba(0,245,255,0.2), inset 0 0 15px rgba(0,245,255,0.05); }
    }
    @keyframes borderPulse {
        0%, 100% { border-color: var(--neon-cyan); box-shadow: 0 0 8px var(--neon-cyan); }
        50%       { border-color: var(--neon-pink);  box-shadow: 0 0 18px var(--neon-pink); }
    }
    @keyframes statusBlink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes scanBar {
        0%   { transform: translateY(-100%); opacity: 0.6; }
        100% { transform: translateY(1000%); opacity: 0; }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    /* ========== HEADER ========== */
    .hero-container {
        text-align: center;
        padding: 10px 0 30px;
        position: relative;
        overflow: hidden;
    }
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.6rem;
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
        font-size: 0.85rem;
        letter-spacing: 3px;
        margin-top: 6px;
        text-shadow: 0 0 10px var(--neon-cyan);
    }
    .divider-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
        margin: 15px auto;
        width: 60%;
    }

    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060a12 0%, #020508 100%) !important;
        border-right: 1px solid rgba(0,245,255,0.2);
        box-shadow: 4px 0 30px rgba(0, 245, 255, 0.06);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* Sidebar Title */
    .sidebar-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--neon-cyan);
        text-align: center;
        letter-spacing: 4px;
        text-shadow: 0 0 14px var(--neon-cyan);
        padding: 10px 0;
    }
    .sidebar-tagline {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: rgba(0,245,255,0.5);
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 16px;
    }

    /* Status Card */
    .status-card {
        background: rgba(0, 20, 35, 0.8);
        border: 1px solid rgba(0, 245, 255, 0.25);
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 12px;
        animation: fadeSlideUp 0.6s ease-out;
    }
    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .status-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: rgba(0,245,255,0.5);
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .status-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: var(--neon-green);
        font-weight: bold;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--neon-green);
        box-shadow: 0 0 8px var(--neon-green);
        margin-right: 6px;
        animation: statusBlink 1.5s infinite;
    }
    .model-badge {
        font-family: 'Share Tech Mono', monospace;
        background: rgba(0,245,255,0.1);
        border: 1px solid rgba(0,245,255,0.3);
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 0.72rem;
        color: var(--neon-cyan);
        text-align: center;
        margin-top: 6px;
        letter-spacing: 1px;
    }

    /* Sidebar divider */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
        margin: 14px 0;
    }

    /* Session stats */
    .session-stats {
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
    }
    .stat-box {
        flex: 1;
        background: rgba(0,30,45,0.6);
        border: 1px solid rgba(0,245,255,0.2);
        border-radius: 5px;
        padding: 10px 8px;
        text-align: center;
    }
    .stat-num {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        color: var(--neon-cyan);
        line-height: 1;
    }
    .stat-label {
        font-size: 0.6rem;
        color: rgba(0,245,255,0.45);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: transparent !important;
        color: var(--neon-pink) !important;
        border: 1px solid var(--neon-pink) !important;
        border-radius: 4px !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 2px;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        transition: all 0.25s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: rgba(255, 0, 200, 0.15) !important;
        box-shadow: 0 0 14px rgba(255, 0, 200, 0.4);
        transform: translateY(-1px);
    }

    /* ========== CHAT MESSAGES ========== */
    [data-testid="stChatMessage"] {
        background: var(--card-bg) !important;
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-left: 3px solid var(--neon-cyan);
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(6px);
        animation: fadeSlideUp 0.4s ease-out;
        box-shadow: 0 2px 12px rgba(0,0,0,0.4), inset 0 0 20px rgba(0,245,255,0.02);
    }
    [data-testid="stChatMessage"][data-testid*="user"] {
        border-left: 3px solid var(--neon-pink) !important;
        background: rgba(30, 0, 30, 0.8) !important;
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
        border-radius: 0 !important;
        color: var(--neon-cyan) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px;
        caret-color: var(--neon-cyan);
        caret-shape: block;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(0, 245, 255, 0.3) !important;
        letter-spacing: 2px;
        font-style: italic;
    }
    /* Send Button */
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
    /* Bottom decorative bar above input */
    .input-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: rgba(0, 245, 255, 0.4);
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 6px;
        text-transform: uppercase;
    }

    /* ========== INFO ALERTS ========== */
    .stAlert {
        background: rgba(0, 245, 255, 0.07) !important;
        border: 1px solid rgba(0,245,255,0.25) !important;
        border-radius: 4px !important;
        color: var(--neon-cyan) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem !important;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #04050d; }
    ::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <p class="main-header">Neural Interface</p>
    <div class="divider-line"></div>
    <p class="sub-header">[ SECURE CHANNEL ACTIVE ] &nbsp;|&nbsp; GROQ LPU ENGINE &nbsp;|&nbsp; LLAMA-3.1 CORE</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
api_key = st.secrets.get("GROQ_API_KEY")
selected_model = "llama-3.1-8b-instant"

# Count messages for session stats (exclude greeting)
msg_count = len([m for m in st.session_state.get("messages", []) if m["role"] == "user"])

with st.sidebar:
    st.markdown('<div class="sidebar-logo">N.I. SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">NEURAL INTERFACE v1.0.0</div>', unsafe_allow_html=True)

    # Connection status
    st.markdown(f"""
    <div class="status-card">
        <div class="status-row">
            <span class="status-label">Status</span>
            <span class="status-value"><span class="status-dot"></span>ONLINE</span>
        </div>
        <div class="status-row">
            <span class="status-label">Uplink</span>
            <span class="status-value" style="color:#00f5ff;">GROQ API</span>
        </div>
        <div class="status-row">
            <span class="status-label">Latency</span>
            <span class="status-value">&lt; 500ms</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active model
    st.markdown(f"""
    <div class="status-card">
        <div class="status-label" style="margin-bottom:8px; color:rgba(0,245,255,0.7);">Active Core</div>
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
            <div class="stat-num">{len(st.session_state.get("messages", []))}</div>
            <div class="stat-label">Messages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Purge button
    if st.button("PURGE MEMORY", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Memory purged. Awaiting new command input..."}
        ]
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center; font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:rgba(0,245,255,0.25); line-height:1.8;">
        BUILT WITH STREAMLIT<br>
        POWERED BY GROQ<br>
        &copy; 2026 N.I. SYSTEMS
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT INTERFACE ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Connection established. Neural core online. How can I assist you, operator?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Decorative label above input
st.markdown('<div class="input-label">// input terminal — type your query below</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Enter command..."):
    if not api_key:
        st.error("ERR_401 // API KEY NOT FOUND IN SECRETS.TOML")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            client = Groq(api_key=api_key)
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            completion = client.chat.completions.create(
                model=selected_model,
                messages=api_messages,
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "█")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()  # refresh stats in sidebar
        except Exception as e:
            st.error(f"SYS_ERR // {e}")
