from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from engine.reasoner import LLMReasoner

app = FastAPI()
reasoner = LLMReasoner()

class UserRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: UserRequest):
    try:
        result = await reasoner.decide_and_execute(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
