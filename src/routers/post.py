from fastapi import (
    FastAPI, 
    HTTPException , 
    status , 
    Response,
    Depends,
    APIRouter
)
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models , schemas
from ..oauth2 import get_current_user


router = APIRouter()

@router.get(
    "", 
    response_model=List[schemas.PostView]
)
def get_post(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    search : Optional[str] = "" # query parameter
):
    posts = db.query(models.Post).filter(
            models.Post.title.contains(search)
        )

    posts = posts.all()

    
    return posts

@router.post(
    "", 
    status_code = status.HTTP_201_CREATED
)
def createpost(
    post: schemas.Post ,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_post = models.Post(**post.dict())
    new_post.author_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data" : new_post}

@router.get(
    "/{id}",
    response_model=schemas.PostView
)
def get_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post found"
        )
    return get_post

@router.delete(
    "/{id}", 
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post found"
        )
        
    if get_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not permitted"
        )
    db.delete(get_post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put(
    "/{id}"
)
def update_post(
    id: int, 
    post: schemas.Post, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post found"
        )
    
    if get_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not permitted"
        )

    for key,value in post.dict().items():
        setattr(get_post, key, value)

    get_post.author_id = current_user.id
    db.add(get_post)
    db.commit()
    db.refresh(get_post)

    return get_post
