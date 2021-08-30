from typing import List
from fastapi import FastAPI, Depends, status, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from .database import SessionLocal, engine
from . import schemas, models
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code= status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title= request.title, body= request.body, user_id= 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def get_by_id(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'The blog with the id: {id} was not found')
    return blog

@app.delete('/blog/{id}',status_code= status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog qith the id {id} was not found')        

    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done'

@app.put('/blog/{id}',status_code= status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog=  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog qith the id {id} was not found')
    blog.update({'title': request.title,'body':request.body})
    db.commit()
    return 'updated'


@app.post('/User', response_model= schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email=request.email, password= Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/User/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user with the id {id} was not found')
    return user
    