from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, info

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(info.router)



@app.get('/')
def home():
    return {'message': 'Hello world'}




