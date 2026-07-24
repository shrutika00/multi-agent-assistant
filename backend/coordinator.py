import time
from typing import Dict, Any
from research_agent import run_research
from fact_checker_agent import run_fact_check
from summary_agent import run_summary
from qa_agent import run_qa

def orchestrate_workflow(question: str) -> Dict[str, Any]:
    """
    Orchestrates the multi-agent workflow:
    Research Agent -> Fact Checker Agent -> Summary Agent -> QA Agent
    Measures execution time for each agent and generates step-by-step progress logs.
    """
    steps = []
    execution_time = {}
    
    # 1. Research Agent Execution
    research_start = time.time()
    steps.append({
        "agent": "Research Agent",
        "status": "Running",
        "message": "Analyzing request and compiling structured research notes..."
    })
    try:
        research_notes = run_research(question)
        research_duration = time.time() - research_start
        execution_time["research"] = f"{research_duration:.2f}s"
        steps.append({
            "agent": "Research Agent",
            "status": "Completed",
            "message": f"Research notes generated successfully in {execution_time['research']}."
        })
    except Exception as e:
        steps.append({
            "agent": "Research Agent",
            "status": "Failed",
            "message": f"Research failed: {str(e)}"
        })
        raise Exception(f"Research Agent failed: {str(e)}")

    # 2. Fact Checker Agent Execution
    fact_check_start = time.time()
    steps.append({
        "agent": "Fact Checker Agent",
        "status": "Running",
        "message": "Reviewing research notes for inaccuracies and logical consistency..."
    })
    try:
        fact_check_notes = run_fact_check(research_notes)
        fact_check_duration = time.time() - fact_check_start
        execution_time["fact_check"] = f"{fact_check_duration:.2f}s"
        steps.append({
            "agent": "Fact Checker Agent",
            "status": "Completed",
            "message": f"Fact checking completed successfully in {execution_time['fact_check']}."
        })
    except Exception as e:
        steps.append({
            "agent": "Fact Checker Agent",
            "status": "Failed",
            "message": f"Fact checking failed: {str(e)}"
        })
        raise Exception(f"Fact Checker Agent failed: {str(e)}")

    # 3. Summary Agent Execution
    summary_start = time.time()
    steps.append({
        "agent": "Summary Agent",
        "status": "Running",
        "message": "Synthesizing research notes and verified notes into a concise draft..."
    })
    try:
        summary_draft = run_summary(research_notes, fact_check_notes)
        summary_duration = time.time() - summary_start
        execution_time["summary"] = f"{summary_duration:.2f}s"
        steps.append({
            "agent": "Summary Agent",
            "status": "Completed",
            "message": f"Summary draft created successfully in {execution_time['summary']}."
        })
    except Exception as e:
        steps.append({
            "agent": "Summary Agent",
            "status": "Failed",
            "message": f"Summarization failed: {str(e)}"
        })
        raise Exception(f"Summary Agent failed: {str(e)}")

    # 4. QA Agent Execution
    qa_start = time.time()
    steps.append({
        "agent": "Quality Assurance Agent",
        "status": "Running",
        "message": "Verifying completeness, tone, and polishing the final response..."
    })
    try:
        final_answer = run_qa(question, summary_draft)
        qa_duration = time.time() - qa_start
        execution_time["quality_assurance"] = f"{qa_duration:.2f}s"
        steps.append({
            "agent": "Quality Assurance Agent",
            "status": "Completed",
            "message": f"Quality assurance completed successfully in {execution_time['quality_assurance']}."
        })
    except Exception as e:
        steps.append({
            "agent": "Quality Assurance Agent",
            "status": "Failed",
            "message": f"Quality assurance failed: {str(e)}"
        })
        raise Exception(f"Quality Assurance Agent failed: {str(e)}")

    # Calculate total duration
    total_duration = research_duration + fact_check_duration + summary_duration + qa_duration
    execution_time["total"] = f"{total_duration:.2f}s"

    return {
        "question": question,
        "research": research_notes,
        "fact_check": fact_check_notes,
        "summary": summary_draft,
        "final_answer": final_answer,
        "steps": steps,
        "execution_time": execution_time
    }
