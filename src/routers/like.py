from fastapi import (
    FastAPI, 
    HTTPException , 
    status , 
    Response,
    Depends,
    APIRouter
)
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models , schemas
from ..oauth2 import get_current_user


router = APIRouter()

@router.post("", status_code = status.HTTP_201_CREATED)
def like(
    like: schemas.Like ,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_post = db.query(models.Post).filter(
        models.Post.id == like.post_id
    ).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post found"
        )
        
    db_like = db.query(models.Like).filter(
        models.Like.post_id == like.post_id,
        models.Like.user_id == current_user.id
    ).first()

    if db_like:
        db.delete(db_like)
        db.commit()

        return {"message": "Unliked"}
    else:
        add_like = models.Like(
            post_id = like.post_id,
            user_id = current_user.id
        )
        db.add(add_like)
        db.commit()
        db.refresh(add_like)

        return {"message": "Liked"}
