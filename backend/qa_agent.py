from llm import generate_text

SYSTEM_PROMPT = """You are a Quality Assurance (QA) Agent.
Your role is to perform the final review and polish on the summary draft.
You must ensure:
1. Completeness: The answer fully addresses the original user request.
2. Readability: The language is natural, engaging, and professional.
3. Clarity and Inconsistencies: Fix any awkward phrasing, confusing structures, or formatting issues.

Produce the final, polished response that is ready to be presented to the user."""

def run_qa(original_question: str, summary_draft: str) -> str:
    """
    Executes the Quality Assurance Agent. Evaluates the summary draft against the original question,
    performs final edits, and returns a fully polished response.
    """
    prompt = f"""Original User Request: {original_question}

Summary Draft to Review:
---
{summary_draft}
---

Please review the summary draft. Ensure it fully answers the request, improve readability, remove any final inconsistencies, and output the final polished response."""
    return generate_text(prompt, system_instruction=SYSTEM_PROMPT)
