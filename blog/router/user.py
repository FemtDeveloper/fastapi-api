from blog.repository.user import create_new_user, get_user_by_id
from blog.database import get_db
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from blog import schemas
from fastapi import APIRouter


router = APIRouter(
    prefix='/User',
 tags=['users']
)

@router.post('/', response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return create_new_user(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id:int,db: Session = Depends(get_db)):
    return get_user_by_id(id, db)
    