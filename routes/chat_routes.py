from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from db import get_db
from models import ChatHistory, ChatMessage, User
from schemas.Chat_schemas import ChatCreate, ChatResponse, ChatWithMessages, MessageCreate, MessageResponse
from utils.security import get_current_user

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)

@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_chat = ChatHistory(user_id=current_user.id, title=chat.title)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get("/", response_model=List[ChatResponse])
def get_chats(q: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Base query for user's chats
        query = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id)
        
        if q:
            # Search in title or in message content
            # We use distinct to avoid multiple rows for the same chat if multiple messages match
            query = query.outerjoin(ChatMessage).filter(
                (ChatHistory.title.ilike(f"%{q}%")) |
                (ChatMessage.content.ilike(f"%{q}%"))
            ).distinct()
            
        return query.order_by(ChatHistory.updated_at.desc()).all()
    except Exception as e:
        print(f"ERROR in get_chats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chat_id}",response_model=ChatWithMessages)
def get_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id, ChatHistory.user_id == current_user.id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        return chat
    except Exception as e:
        print(f"ERROR fetching chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{chat_id}/messages", response_model=MessageResponse)
def add_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id, ChatHistory.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    new_message = ChatMessage(chat_id=chat_id, role=message.role, content=message.content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    chat.updated_at = new_message.created_at
    db.commit()
    return new_message

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id, ChatHistory.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    return None
