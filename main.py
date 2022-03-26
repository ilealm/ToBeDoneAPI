# from lib2to3.pgen2.token import OP
# from re import I
from typing import Optional   #for the user model here
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Authentication and Authorizaion
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# for verifying tokens JSON Web Tokens(jwt)
from jose import JWTError, jwt
# for token expiration
from datetime import datetime, timedelta
# Hash and verify passwords
from passlib.context import CryptContext
# Authentication and Authorizaion, in this example
from pydantic import BaseModel

from model import Users



app = FastAPI()
# this import has to be after the creation of app, BC is referenced in the next import
# from routes import user_routes
from routes import (
    # task_routes,
    user_routes
    )

# from routes import test_task_routes
# CORS: Specify the Origins of React and FastAPI so they can communicate.
# If I don't do this, they WON'T communitate!
# React port: 3000   /   FastAPI port :8000 (That's why is 127.0.0.1:8000)
# TODO add this to settings
origins = [
    'https://localhost:3000',
    'http://localhost:3000',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

