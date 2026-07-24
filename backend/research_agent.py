from llm import generate_text

SYSTEM_PROMPT = """You are a highly analytical Research Agent.
Your role is to break down the user's request, perform deep conceptual analysis, and compile detailed research notes.
Focus on:
1. Explaining core concepts clearly.
2. Breaking down the problem into logical parts or structured bullet points.
3. Providing context and detailed explanations for each point.

Format your output in a structured, comprehensive manner using clean Markdown headings and lists."""

def run_research(question: str) -> str:
    """
    Executes the Research Agent. Takes a user question, makes an independent LLM call,
    and returns detailed research notes.
    """
    prompt = f"User Request: {question}\n\nPlease perform detailed research and provide structured notes for this request."
    return generate_text(prompt, system_instruction=SYSTEM_PROMPT)
