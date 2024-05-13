import src.settings as settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from src.api import auth, cart

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=settings.DATABASE_CONFIG,
    add_exception_handlers=True,
)

app.include_router(auth.router)

app.include_router(cart.router)
