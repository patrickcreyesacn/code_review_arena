# ⚔️ Code Review Arena
### Multi-Agent AI Code Analysis System

A **Gen AI Bootcamp Capstone** project — a multi-agent system where AI agents independently review code and a Judge synthesizes the final verdict.

---

## 🏗️ Architecture

```
User Input (code + context)
        ↓
[runs in parallel]
Agent 1: Security Reviewer     Agent 2: Performance Reviewer
        ↓                               ↓
        └───────── Agent 3: Judge ──────┘
                        ↓
          Final Verdict + Score + Fixes
```

## 🤖 Agent Roles

| Agent | Role | Analyzes |
|-------|------|----------|
| **Agent 1 — Security Reviewer** | Red team security audit | Injections, auth flaws, hardcoded secrets, input validation |
| **Agent 2 — Performance Reviewer** | Efficiency & quality audit | Time complexity, memory, anti-patterns, maintainability |
| **Agent 3 — Judge** | Synthesizer & verdict | Combines both scores, top 3 fixes, final recommendation |

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your free Gemini API key
-Go to: https://aistudio.google.com/app/apikey
-Copy the generated API key
-Then create .env file inside the project folder and type GEMINI_API_KEY=[paste Gemini API key here]


### 3. Run the app
```bash
streamlit run app.py
```

### 4. Use the app
1. Enter your Gemini API key
2. Select programming language
3. Describe what your code does (context)
4. Paste your code
5. Click **Run Code Review Arena**
6. Get parallel agent reviews + final verdict

## 📁 Project Structure

```
code_arena/
├── app.py                      # Streamlit UI + orchestration
├── agents/
│   ├── __init__.py
│   ├── security_agent.py       # Agent 1: Security Reviewer
│   ├── performance_agent.py    # Agent 2: Performance Reviewer
│   └── judge_agent.py          # Agent 3: Judge / Synthesizer
├── requirements.txt
└── README.md
```

## 🔧 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Google Gemini 1.5 Flash (via `google-generativeai`)
- **Agent Pattern:** Parallel execution (threading) + sequential judge

## 📊 Scoring

- Security Score: 0–100
- Performance Score: 0–100
- **Final Score** = (Security × 0.5) + (Performance × 0.5)
- Grade: A (90–100) / B (80–89) / C (70–79) / D (60–69) / F (<60)

## 👥 Team

Gen AI Bootcamp — FY26 Capstone
Presentation: March 19, 2026
