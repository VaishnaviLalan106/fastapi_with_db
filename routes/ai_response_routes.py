from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import ChatHistory, ChatMessage, User
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse
from utils.security import get_current_user

router = APIRouter()


@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get response from AI model and store in chat history."""
    try:
        # 1. Determine or create chat
        chat_id = request.chat_id
        if not chat_id and request.title:
            # Create new chat if title provided
            new_chat = ChatHistory(user_id=current_user.id, title=request.title)
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            chat_id = new_chat.id
        
        if chat_id:
            # Verify chat existence and ownership
            chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id, ChatHistory.user_id == current_user.id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found or access denied")
            
            # 2. Store user message
            user_msg = ChatMessage(chat_id=chat_id, role="user", content=request.message)
            db.add(user_msg)
            
        # 3. Get AI completion
        ai_content = get_completion(request.message, request.system_prompt)
        
        if chat_id:
            # 4. Store AI response
            ai_msg = ChatMessage(chat_id=chat_id, role="assistant", content=ai_content)
            db.add(ai_msg)
            
            # Update chat's updated_at
            from datetime import datetime
            chat.updated_at = datetime.utcnow()
            
            db.commit()
            
        return AIResponse(response=ai_content, chat_id=chat_id)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))