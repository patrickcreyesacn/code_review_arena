import streamlit as st
import threading
import os
import sys
from dotenv import load_dotenv

# Ensure project root is in path so 'agents' module is always found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.security_agent import run_security_agent
from agents.performance_agent import run_performance_agent
from agents.judge_agent import run_judge_agent

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Code Review Arena",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg:       #0a0a0f;
    --surface:  #111118;
    --border:   #1e1e2e;
    --accent1:  #ff4d6d;
    --accent2:  #00d4ff;
    --accent3:  #f4c430;
    --text:     #e8e8f0;
    --muted:    #6b6b80;
    --green:    #00ff9f;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: var(--bg);
}

[data-testid="stSidebar"] { background-color: var(--surface) !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.2rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 50%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Cards ── */
.agent-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.agent-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.agent-card.security::before  { background: var(--accent1); }
.agent-card.performance::before { background: var(--accent2); }
.agent-card.judge::before     { background: var(--accent3); }

.agent-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.agent-label.security  { color: var(--accent1); }
.agent-label.performance { color: var(--accent2); }
.agent-label.judge     { color: var(--accent3); }

.agent-title {
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
}

.review-output {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c8c8d8;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Score badge ── */
.score-ring {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 90px; height: 90px;
    border-radius: 50%;
    border: 3px solid var(--accent3);
    margin: 0 auto 1rem;
}
.score-num {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--accent3);
    line-height: 1;
}
.score-lbl {
    font-size: 0.6rem;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
}

/* ── Status chips ── */
.chip {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
    font-weight: 700;
    text-transform: uppercase;
    margin: 0.2rem 0.2rem 0.2rem 0;
}
.chip-red    { background: rgba(255,77,109,0.15); color: var(--accent1); border: 1px solid var(--accent1); }
.chip-blue   { background: rgba(0,212,255,0.15);  color: var(--accent2); border: 1px solid var(--accent2); }
.chip-yellow { background: rgba(244,196,48,0.15); color: var(--accent3); border: 1px solid var(--accent3); }
.chip-green  { background: rgba(0,255,159,0.15);  color: var(--green);   border: 1px solid var(--green); }

/* ── Input panel ── */
.input-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextArea"] textarea {
    background: #0d0d14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
[data-testid="stTextInput"] input {
    background: #0d0d14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent2) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #0d0d14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
label, [data-testid="stWidgetLabel"] {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent1), #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,77,109,0.4) !important;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] { color: var(--accent2) !important; }

/* ── Architecture diagram ── */
.arch-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 2;
}
.arch-node {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 6px;
    font-weight: 700;
    margin: 0.1rem;
}
.node-user   { background: rgba(107,107,128,0.2); color: var(--text); border: 1px solid var(--muted); }
.node-sec    { background: rgba(255,77,109,0.15); color: var(--accent1); border: 1px solid var(--accent1); }
.node-perf   { background: rgba(0,212,255,0.15);  color: var(--accent2); border: 1px solid var(--accent2); }
.node-judge  { background: rgba(244,196,48,0.15); color: var(--accent3); border: 1px solid var(--accent3); }
.node-output { background: rgba(0,255,159,0.15);  color: var(--green);   border: 1px solid var(--green); }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">⚔️ Code Review Arena</div>
    <div class="hero-sub">Multi-Agent AI Code Analysis System</div>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── Architecture diagram ───────────────────────────────────────────────────────
with st.expander("📐 System Architecture", expanded=False):
    st.markdown("""
    <div class="arch-box">
        <span class="arch-node node-user">👤 User Input</span><br>
        ↓<br>
        <span style="color:var(--muted); font-size:0.75rem;">runs in parallel</span><br>
        <span class="arch-node node-sec">🔒 Agent 1 — Security Reviewer</span>
        &nbsp;&nbsp;&nbsp;
        <span class="arch-node node-perf">⚡ Agent 2 — Performance Reviewer</span><br>
        ↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <span class="arch-node node-judge">⚖️ Agent 3 — Judge (Synthesizer)</span><br>
        ↓<br>
        <span class="arch-node node-output">✅ Final Verdict + Score + Fixes</span>
    </div>
    """, unsafe_allow_html=True)

# ── API Key check ─────────────────────────────────────────────────────────────
if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found. Add it to your `.env` file: `GEMINI_API_KEY=your_key_here`")
    st.stop()

# ── Input panel ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-panel">', unsafe_allow_html=True)

language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "go", "rust", "c++", "c#", "php", "ruby"])

context = st.text_input("📝 Context (what does this code do?)", placeholder="e.g. User login endpoint for a web app")

code_input = st.text_area(
    "💻 Paste your code here",
    height=280,
    placeholder="# Paste your code here...\ndef login(username, password):\n    query = f\"SELECT * FROM users WHERE name='{username}'\"\n    ..."
)

run_btn = st.button("⚔️ Run Code Review Arena")
st.markdown('</div>', unsafe_allow_html=True)

# ── Run agents ────────────────────────────────────────────────────────────────
if run_btn:
    if not code_input.strip():
        st.error("⚠️ Please paste some code to review.")
    else:
        results = {}
        errors = {}

        def run_security(key, code, lang, ctx):
            try:
                results["security"] = run_security_agent(key, code, lang, ctx)
            except Exception as e:
                errors["security"] = str(e)

        def run_performance(key, code, lang, ctx):
            try:
                results["performance"] = run_performance_agent(key, code, lang, ctx)
            except Exception as e:
                errors["performance"] = str(e)

        # ── Stage 1: Parallel agents ──
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0; font-family:'JetBrains Mono',monospace; color:var(--muted); font-size:0.8rem;">
            <span class="chip chip-red">Agent 1</span>
            <span class="chip chip-blue">Agent 2</span>
            &nbsp; Running in parallel...
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("🔒 Security & ⚡ Performance agents analyzing your code..."):
            t1 = threading.Thread(target=run_security,    args=(API_KEY, code_input, language, context))
            t2 = threading.Thread(target=run_performance, args=(API_KEY, code_input, language, context))
            t1.start(); t2.start()
            t1.join();  t2.join()

        if errors:
            for agent, err in errors.items():
                st.error(f"❌ {agent.capitalize()} Agent error: {err}")
        
        if "security" in results and "performance" in results:
            # ── Stage 2: Judge ──
            with st.spinner("⚖️ Judge Agent synthesizing final verdict..."):
                try:
                    results["judge"] = run_judge_agent(
                        API_KEY,
                        results["security"],
                        results["performance"],
                        code_input,
                        language
                    )
                except Exception as e:
                    st.error(f"❌ Judge Agent error: {e}")
                    st.stop()

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align:center; margin-bottom:1.5rem;">
                <span style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; color:var(--text);">
                    Review Complete
                </span>
            </div>
            """, unsafe_allow_html=True)

            # ── Output: 3 columns ──
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="agent-card security">
                    <div class="agent-label security">Agent 01 — Security</div>
                    <div class="agent-title">🔒 Security Reviewer</div>
                    <div class="review-output">{results["security"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="agent-card performance">
                    <div class="agent-label performance">Agent 02 — Performance</div>
                    <div class="agent-title">⚡ Performance Reviewer</div>
                    <div class="review-output">{results["performance"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="agent-card judge">
                    <div class="agent-label judge">Agent 03 — Judge</div>
                    <div class="agent-title">⚖️ Final Verdict</div>
                    <div class="review-output">{results["judge"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Download ──
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            full_report = f"""CODE REVIEW ARENA — FULL REPORT
{'='*60}
Language: {language}
Context: {context}
{'='*60}

AGENT 1 — SECURITY REVIEW
{'-'*60}
{results['security']}

AGENT 2 — PERFORMANCE REVIEW  
{'-'*60}
{results['performance']}

AGENT 3 — JUDGE VERDICT
{'-'*60}
{results['judge']}
"""
            st.download_button(
                label="📥 Download Full Report",
                data=full_report,
                file_name="code_review_report.txt",
                mime="text/plain"
            )