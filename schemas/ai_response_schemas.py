from pydantic import BaseModel
from typing import Optional, List

class HistoryMessage(BaseModel):
    role: str
    content: str

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    chat_id: Optional[int] = None
    title: Optional[str] = None
    history: Optional[List[HistoryMessage]] = None

class AIResponse(BaseModel):
    response: str
    chat_id: Optional[int] = None

class TitleRequest(BaseModel):
    chat_id: int
    user_message: str
    ai_response: str

class TitleResponse(BaseModel):
    title: str