from typing import List
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
from .. import models , schemas , utils

router = APIRouter()

@router.post("", status_code = status.HTTP_201_CREATED)
def create_user(user:schemas.User, db: Session = Depends(get_db)):

    # hasing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data" : new_user}

@router.get("", response_model=List[schemas.UserView])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users



@router.get("/{id}", response_model=schemas.UserView)
def get_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found"
        )
    return get_user

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found"
        )
    
    db.delete(get_user)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found"
        )
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    for key,value in user.dict().items():
        setattr(get_user, key, value)

    db.add(get_user)
    db.commit()
    db.refresh(get_user)

    return get_user
