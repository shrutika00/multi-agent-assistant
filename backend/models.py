from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    message: str

class StepInfo(BaseModel):
    agent: str
    status: str
    message: str

class ExecutionTime(BaseModel):
    research: str
    fact_check: str
    summary: str
    quality_assurance: str
    total: str

class ChatResponse(BaseModel):
    question: str
    research: str
    fact_check: str
    summary: str
    final_answer: str
    steps: List[StepInfo]
    execution_time: ExecutionTime
