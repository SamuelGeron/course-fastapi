from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)

# Commented as now using ALEMBIC to handle changes in the metadata
# SETUP THE DATABASE
# models.Base.metadata.create_all(bind=engine)

# STARTING UP THE API
app = FastAPI()

# CORS Policy - Cross-Origin Resource Sharing
origins = ["https://www.google.com", "https://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- DECORATORS -------
# GET ROOT
@app.get("/")
async def root():
    return {"message": "Welcome to my API BRO"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


