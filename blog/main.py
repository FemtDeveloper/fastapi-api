from fastapi import FastAPI
from sqlalchemy.sql.functions import user
from .database import engine
from . import models
from .router import blog, user, authentication


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
#Now we can deploy