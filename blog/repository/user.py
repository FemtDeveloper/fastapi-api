from fastapi.exceptions import HTTPException
from blog.hashing import Hash
from blog import models, schemas
from sqlalchemy.orm.session import Session
from fastapi import status

def create_new_user(request: schemas.User, db: Session):
    new_user = models.User(name = request.name, email=request.email, password= Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user with the id {id} was not found')
    return user
    