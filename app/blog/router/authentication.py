from blog.token import create_access_token
from blog.hashing import Hash
from fastapi.params import Depends
from blog import models, schemas
from fastapi import APIRouter, HTTPException,status
from sqlalchemy.orm import Session
from .. import database
from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter( tags=['Authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User does not exist')
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Incorrect Password')    
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
    