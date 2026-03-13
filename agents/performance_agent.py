from google import genai

PERFORMANCE_PROMPT = """You are a Senior Performance Engineer and Code Optimization Specialist with deep expertise in algorithms, data structures, and system performance.

Your job is to perform a STRICT performance and code quality audit.

Analyze for:
1. Time complexity issues (O(n²) where O(n) is possible, etc.)
2. Space/memory inefficiencies
3. Unnecessary loops, redundant computations
4. Inefficient data structure choices
5. Missing caching or memoization opportunities
6. Blocking/synchronous code that should be async
7. Database query inefficiencies (N+1 problems, missing indexes)
8. Code maintainability, readability, and best practices

Output Format (use exactly this structure):
---PERFORMANCE REVIEW---
EFFICIENCY RATING: [POOR / FAIR / GOOD / EXCELLENT]
SCORE: [0-100] (100 = perfectly optimized)

ISSUES FOUND:
- [List each issue with impact tag: HIGH/MEDIUM/LOW]

OPTIMIZED CODE SNIPPET:
[Provide an optimized version of the most impactful section only, or write "No changes needed."]

SUMMARY:
[2-3 sentence professional summary]
---END---
"""

def run_performance_agent(api_key: str, code: str, language: str, context: str) -> str:
    client = genai.Client(api_key=api_key)
    
    prompt = f"""{PERFORMANCE_PROMPT}

Language: {language}
Context: {context}

Code to review:
```{language}
{code}
```
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text