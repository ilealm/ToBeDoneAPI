from http.client import REQUEST_URI_TOO_LONG
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

# from dotenv import dotenv_values
from dotenv import dotenv_values
from model import Users



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=dotenv_values(".env")["ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# this import has to be after the creation of app, BC is referenced in the next import

from routes import (    
    auth,
    )
