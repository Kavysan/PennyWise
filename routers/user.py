from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List
import hashing
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=['users'],
    prefix='/user'
)

templates = Jinja2Templates(directory="templates")

@router.post('/', status_code=status.HTTP_201_CREATED)
def add_user(request: schemas.AddUser ,db:Session = Depends(get_db)):
    new_user =  models.UserTable(name=request.name, email=request.email, password=hashing.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', status_code=status.HTTP_202_ACCEPTED, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserTable).all()

@router.get('/{id}', status_code= status.HTTP_202_ACCEPTED, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserTable).filter(models.UserTable.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not a valid user id")
    return user

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int,  request: schemas.AddUser ,db: Session = Depends(get_db)):
    user_query = db.query(models.UserTable).filter(models.UserTable.id==id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not a vaild id")
    user_query.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return {"detail":"updated user details"}

@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.UserTable).filter(models.UserTable.id==id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not a vaild id")
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"detail":"deleted user details"}

    
