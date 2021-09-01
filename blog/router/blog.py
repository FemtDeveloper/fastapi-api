from blog.repository.blog import create_blog, delete_blog, get_blog_by_id, getall, update_blog
from sqlalchemy.orm.session import Session
from blog.database import get_db
from fastapi.param_functions import Depends
from blog import schemas
from typing import List
from fastapi import APIRouter, status
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db), current_user: schemas.User =  Depends(get_current_user)):
    return getall(db)

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User =  Depends(get_current_user)):
    return create_blog(request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_by_id(id, db: Session = Depends(get_db), current_user: schemas.User =  Depends(get_current_user)):
    return get_blog_by_id(id, db)


@router.put('/{id}',status_code= status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User =  Depends(get_current_user)):
    return update_blog(id, request, db)
    

@router.delete('/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete_by_id(id, db: Session = Depends(get_db), current_user: schemas.User =  Depends(get_current_user)):
    return delete_blog(id, db)
