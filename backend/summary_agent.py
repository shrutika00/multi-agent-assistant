from llm import generate_text

SYSTEM_PROMPT = """You are a Summary Agent.
Your role is to read both the Research Notes and the Fact Checker's Verified Notes, and synthesize them into a concise, unified draft.
Ensure that:
1. You resolve any inaccuracies flagged by the Fact Checker using their corrections.
2. You eliminate all repetitions and redundant arguments.
3. The explanation flows logically and is easy to follow.

Write a clear, structured draft combining the verified facts and research insights."""

def run_summary(research_notes: str, fact_check_notes: str) -> str:
    """
    Executes the Summary Agent. Receives both the research notes and fact-check notes,
    and returns a clean, synthesized summary draft.
    """
    prompt = f"""Research Notes:
---
{research_notes}
---

Fact Checker Verified Notes:
---
{fact_check_notes}
---

Please combine and synthesize the above research and fact-check notes into a concise, unified, and error-free summary."""
    return generate_text(prompt, system_instruction=SYSTEM_PROMPT)
