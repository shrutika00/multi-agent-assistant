from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from coordinator import orchestrate_workflow

app = FastAPI(
    title="Multi-Agent Assistant Backend",
    description="FastAPI backend orchestrating Research, Fact Check, Summary, and QA Agents using the Google Gemini API.",
    version="1.0.0"
)

# Enable CORS for local testing from index.html or live servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", summary="Health Check")
def health_check():
    """
    Simple health status endpoint.
    """
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse, summary="Initiate Multi-Agent Workflow")
def chat_endpoint(request: ChatRequest):
    """
    Triggers the multi-agent orchestration pipeline.
    Expects a user query, sequential processes it through agents,
    and returns intermediate results, logs, and timing metrics.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")
        
    try:
        response_data = orchestrate_workflow(request.message)
        return response_data
    except ValueError as val_err:
        # e.g., missing API key
        raise HTTPException(status_code=500, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during workflow execution: {str(e)}")
