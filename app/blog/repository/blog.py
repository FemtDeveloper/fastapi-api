
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from starlette import status
from blog import models, schemas


def getall(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create_blog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title= request.title, body= request.body, user_id= 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    
def get_blog_by_id(id, db: Session):
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'The blog with the id: {id} was not found')
        return blog

def update_blog(id, request:  schemas.Blog, db: Session):
    blog=  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog qith the id {id} was not found')
    blog.update({'title': request.title,'body':request.body})
    db.commit()
    return 'updated'


def delete_blog(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog qith the id {id} was not found')        
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done'
