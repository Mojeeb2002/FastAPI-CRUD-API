import logging
from fastapi import FastAPI, HTTPException, Depends
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from starlette import status
from . import models, schemas
from .database import engine, get_db
from typing import List


app = FastAPI()

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)



def get_db_connection():
    while True:
        try:
            conn = connect(
                host='localhost',
                database='You database name',
                user='Your database user name',
                password='Your database password',
                port=5432,
                cursor_factory=RealDictCursor
            )
            logging.info("Connected to PostgreSQL")
            return conn
        except OperationalError as error:
            logging.error("Failed to connect to PostgreSQL")
            logging.error(error)
            time.sleep(5)

@app.get('/')
def home():
    return {'message': 'Hello world'}


@app.get('/posts', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put('/posts/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}
