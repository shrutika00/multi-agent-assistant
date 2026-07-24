from llm import generate_text

SYSTEM_PROMPT = """You are a critical Fact Checker Agent.
Your role is to review the research notes provided by the Research Agent.
You must inspect the text for:
1. Potential inaccuracies or misleading explanations.
2. Unsupported claims or logical contradictions.
3. Key areas that need correction or clarification.

Provide 'Verified Notes' containing:
- An assessment of the research's correctness (e.g., 'Verification Status: Passed' or 'Verification Status: Edits Suggested').
- A bulleted list of specific corrections or verifications for each point in the research.
- Critical insights that should be clarified."""

def run_fact_check(research_notes: str) -> str:
    """
    Executes the Fact Checker Agent. Takes research notes, performs an independent LLM call,
    and returns verified notes outlining corrections or confirmation.
    """
    prompt = f"Research Notes to Verify:\n---\n{research_notes}\n---\n\nPlease review these research notes, check for errors, and output verified fact-check notes."
    return generate_text(prompt, system_instruction=SYSTEM_PROMPT)
