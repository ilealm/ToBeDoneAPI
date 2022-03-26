import re
from urllib import response
from fastapi import HTTPException, status
from pydantic import EmailStr
from typing import Optional

from main import app
from model import Users
from database import (
    create_user, 
    fetch_all_users,
    fetch_user_by_username,
    update_user,
    remove_user,
)


#  User routes
@app.post("/api/users/", response_model=Users, status_code=status.HTTP_201_CREATED)
async def post_user(user:Users):
    # create the user, which need to be in JSON, so I'm using .dict
    response = await create_user(user.dict())

    if response:
        return response
    raise HTTPException(400, "Something went wrong / bad request.")


    
@app.get("/api/users/")
async def get_users():
    response = await fetch_all_users()
    return response


@app.get("/api/users/{username}", response_model=Users)
async def get_user_by_username(username):
    response = await fetch_user_by_username(username)

    if response:
        return response
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"There is no user with username {username}.")


@app.put("/api/users/{username}", response_model=Users)
async def put_user(username: str, full_name: Optional[str], email: Optional[EmailStr], hashed_password: Optional[str],  disabled: Optional[bool] = False):
    response = await update_user(username, full_name, email, hashed_password, disabled)

    if response:
        return response
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"There is no username {username}.")


# @app.delete("/api/users/{username}", response_model=Users)
@app.delete("/api/users/{username}")
async def delete_user(username):
    response = await remove_user(username)

    if response:
        return f"User {username} succesfully deleted."
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"The user {username} does not exists.")