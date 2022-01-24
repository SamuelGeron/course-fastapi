from lib2to3.pytree import Base
from multiprocessing import connection
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import mysql.connector
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


# SETUP THE DATABASE
models.Base.metadata.create_all(bind=engine)

# STARTING UP THE API
app = FastAPI()



while True:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database='fastapi'
        )
        cursor = conn.cursor(dictionary=True)
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Errror: ", error)
        time.sleep(2)


# ----- FUNCTIONS ------

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# ----- DECORATORS -------

# GET ROOT
@app.get("/")
async def root():
    return {"message": "Welcome to my API BRO"}


# POST
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """,
    #                 (post.title, post.content, post.published))
    # affected_rows = cursor.rowcount
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# GET ALL
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# GET BY ID
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, [id])
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


# PUT 
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s""", (post.title, post.content, post.published, id))
    # affected_rows = cursor.rowcount
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()


# DELETE
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id  = %s """, [id])
    # affected_rows = cursor.rowcount
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




