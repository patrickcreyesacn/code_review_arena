from google import genai

JUDGE_PROMPT = """You are the Chief Code Quality Judge — a principal engineer with 20+ years of experience across security, performance, and software architecture.

You have received two independent expert reviews of the same code:
1. A Security Review
2. A Performance Review

Your job is to synthesize both reviews into a final authoritative verdict.

Scoring:
- Security Score weight: 50%
- Performance Score weight: 50%
- Calculate: Final Score = (security_score * 0.5) + (performance_score * 0.5)

Output Format (use exactly this structure):
---JUDGE VERDICT---
FINAL SCORE: [0-100]
SECURITY SCORE: [from security review]
PERFORMANCE SCORE: [from performance review]
OVERALL GRADE: [A / B / C / D / F]
VERDICT: [SHIP IT ✅ / NEEDS WORK ⚠️ / DO NOT SHIP ❌]

TOP 3 PRIORITY FIXES:
1. [Most critical fix - specify if security or performance]
2. [Second priority fix]
3. [Third priority fix]

FINAL RECOMMENDATION:
[3-4 sentence professional summary combining both reviews. Be direct and actionable.]

BADGE:
[Award ONE badge that best describes this code:
🏆 "Production Ready" | ⚡ "Fast but Risky" | 🔒 "Secure but Slow" | 🚧 "Needs Refactor" | 💣 "Critical Issues" | ✨ "Clean Code"]
---END---
"""

def run_judge_agent(api_key: str, security_review: str, performance_review: str, code: str, language: str) -> str:
    client = genai.Client(api_key=api_key)
    
    prompt = f"""{JUDGE_PROMPT}

Language: {language}

SECURITY REVIEW:
{security_review}

PERFORMANCE REVIEW:
{performance_review}

Original Code:
```{language}
{code}
```
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text