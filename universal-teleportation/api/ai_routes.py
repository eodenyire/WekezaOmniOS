from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/api/ai/chat")
async def chat_with_ai(chat_message: ChatMessage):
    """
    Receives a chat message and returns a simulated AI response.
    """
    user_message = chat_message.message.lower()
    
    # Simulate a delay for a more realistic experience
    await asyncio.sleep(1)

    # Simulated AI responses based on keywords
    if "hello" in user_message:
        response = "Hello! I am the Wekeza OmniOS AI assistant. How can I help you today?"
    elif "create a file" in user_message:
        response = "I can help with that. What should be the name of the file and what content should it have?"
    elif "run code" in user_message:
        response = "Sure, please provide the code you want me to run."
    elif "help" in user_message:
        response = "I can assist with file operations, running code, and answering general questions about the Wekeza OmniOS. What do you need help with?"
    else:
        response = "I'm sorry, I'm not sure how to respond to that. I am still under development. You can ask me to 'create a file', 'run code', or ask for 'help'."

    return {"response": response}
