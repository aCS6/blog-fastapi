from fastapi import (
    APIRouter,
    FastAPI, 
    HTTPException , 
    status , 
    Response,
    Depends
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2, schemas, utils

router = APIRouter()

@router.post("", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    access_token = oauth2.create_access_token(
        data = {"user_id": user.id}
    )
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
    