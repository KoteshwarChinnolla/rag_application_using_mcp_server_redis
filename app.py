from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import asyncio

from src.first_aid_chatbot.client import mcp_server

app = FastAPI()

class MessageRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: MessageRequest):
    response = await mcp_server(request.message)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080)