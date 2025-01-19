from llm_bot_assistant import chat
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="FastAPI Q&A System",
    description="Ask questions based on a dataset about cocktails.",
    version="1.0"
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Endpoint to answer user questions about the dataset and cocktails.
    """
    try:
        answer = chat(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")

@app.get("/")
def api_info():
    return {
        "message": "Welcome to the FastAPI Q&A system for searching cocktails!",
        "endpoints": {
            "ask": "POST /ask - Submit a question about cocktails"
        }
    }
