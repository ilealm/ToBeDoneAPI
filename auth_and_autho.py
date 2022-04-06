from pydantic import BaseModel
from dotenv import dotenv_values
from typing import Optional   #for the user model here
# Authentication and Authorizaion
from fastapi import Depends, HTTPException, status
# using OAuth2, with the Password flow, using a Bearer token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# for verifying tokens JSON Web Tokens(jwt)
from jose import JWTError, jwt
# for token expiration
from datetime import datetime, timedelta
# Hash and verify passwords
from passlib.context import CryptContext



from main import app
from database import(
    fetch_user_by_username
)
# from model import Users

SECRET_KEY = dotenv_values(".env")["SECRET_KEY"]
ALGORITHM = dotenv_values(".env")["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(dotenv_values(".env")["ACCESS_TOKEN_EXPIRE_MINUTES"])

# The frontend sends username and password to a specific URL in our API, declared with tokenUrl="token"
# tokenUrl: contains the URL that the client will use to send the username and password in order to get a token.
# @app.post("/token"..). "token" is the route .../api/token
# tokenURL: client will use to send the username and password in order to get a token.
# tokenUrl instead of token_url?: it's using the same name as in the OpenAPI spec
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# hashing passwords utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# todo delete this fake
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# Pydantic Model that will be used in the token endpoint for the response.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

# * UDATED
# Note: hashed_password MUST BE ENCYPTED using CryptContext, if not, then an error will raise.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# * UDATED
async def get_user(username: str):
    user_dict = await fetch_user_by_username(username)
    # **user_dict transform obj user_dict to a dictionary
    if user_dict:
        return UserInDB(**user_dict) # Pass the keys and values of the user_dict directly as key-value arguments


# * UDATED
async def authenticate_user(username: str, password: str):
    # checking if the user exists
    # ! do I need await here?
    user = await get_user(username)
    # ! check if the next line is correct by me 
    # if I have the user, means in the UserInDB instance already
    if not user:
        return False
    # Check if the password is the same as in DB
    if not verify_password(password, user.hashed_password):
        return False

    return user


# * UDATED
# to this point, the token only has {sub, exp}
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt




# Dependencies can have sub-dependencies:
# get_current_user will have a dependency with the same oauth2_scheme 
# will return a pydantic User model
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # token = str(Depends(oauth2_scheme))
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    # user = get_user(fake_users_db, username=token_data.username)
    # ! i need an await here? I don't think so
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
async def get_current_active_user():
    temp = await get_current_user()
    current_user = User(Depends(temp))
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# * UDATED
# The frontend sends username and password to a specific URL in our API, declared with tokenUrl="token"
# tokenUrl: contains the URL that the client will use to send the username and password in order to get a token.
# @app.post("/token"..). "token" is the resource .../api/token
# This is the resource indicated when created the instance of OAuth2PasswordBearer(tokenUrl="token") 
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") I have dupplicated this line, so I don't believe I need it here
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate if the user exists in the BD and the password is the same.
    user = authenticate_user(form_data.username, form_data.password)
    # user = await authenticate_user(form_data.username, form_data.password)  # maybe I don't need the await here
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # to this point, the user is Authenticaded, so its token will be created 
    # A "token" is just a string with some content that we can use later to verify this user.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
 
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # The response of the token endpoint must be a JSON object.
    # By the spec, you should return a JSON with an access_token and a token_type, the same as in this example.
    # This is something that you have to do yourself in your code, and make sure you use those JSON keys.
    return {"access_token": access_token, "token_type": "bearer"}

# FastAPI calls the get_current_active_user (can be a class o function). 
# This creates an "instance" of that class and the instance will be passed as the parameter User to your function.
# declaring the type (User, in this case) is encouraged as that way your editor will know what will be passed
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# # The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".
# # It could be called as: oauth2_scheme(some, parameters) So, it can be used with Depends.
# # Depends(oauth2_scheme) is telling that the resource must have a securuty scheme. It creates the auth botton
# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]