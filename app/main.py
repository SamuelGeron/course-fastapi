from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import mysql.connector
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post, user, auth


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


# ----- DECORATORS -------

# GET ROOT
@app.get("/")
async def root():
    return {"message": "Welcome to my API BRO"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


