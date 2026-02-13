from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    chat_id: Optional[int] = None
    title: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    chat_id: Optional[int] = None