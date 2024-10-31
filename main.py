from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from engine.reasoner import LLMReasoner

app = FastAPI()
reasoner = LLMReasoner()

class UserRequest(BaseModel):
    user_id: str
    messages: list
    model: str

class AssistantMessage(BaseModel):
    id: str
    role: str
    content: str
    toolInvocations: list = []
    attachments: list = []

@app.post("/chat")
async def chat_endpoint(request: UserRequest):
    try:
        # Extract the latest user message
        user_message = request.messages[-1]['content']

        # Get the assistant's response
        result = await reasoner.decide_and_execute(user_message)

        # Prepare the response
        assistant_message = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": result.get('content', ''),
            "toolInvocations": result.get('toolInvocations', []),
            "attachments": result.get('attachments', []),
        }

        return assistant_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
