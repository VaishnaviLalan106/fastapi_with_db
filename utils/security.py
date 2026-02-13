from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import User
from utils.jwt_handler import verify_token
import os
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt
security=HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"


def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security),db:Session=Depends(get_db)):
    token=credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user_id=int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user
    
    if payload is None:
        raise credentials_exception
    email: str = payload.get("email")
    if email is None:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user
