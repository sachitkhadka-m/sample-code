from fastapi import FastAPI
from .core.database import Base, engine
from app.api.routes import auth, user

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
