from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get('/blog')

def index(limit=10, published: bool=True, sort : Optional[str]=None):
    if published:
        return {'data': 
            f'showing {limit} of Blog list'}
    else:
        return {'data': 
            f'showing Blog list'}


@app.get('/blogs/unpublished')
def unpublished():
    return {'data': 'all the unpublished blogs'}

@app.get('/blogs/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blogs/{id}/comments')
def comments(id):
    return{'data':{'comment 1': 'This is the comment one',
                   'comment 2': 'this is the comment two'}}
    
class Blog(BaseModel):
    title : str
    body: str
    published : Optional[bool]
    

@app.post('/blogs')
def create_blog(blog: Blog):
    return {'data': f'blog created with the title "{blog.title}"'}