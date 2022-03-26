# MongoDB Driver
from curses import curs_set
from pickle import FALSE
import motor.motor_asyncio
from model import (
    Tasks, Users,
)
from dotenv import dotenv_values
from fastapi import HTTPException, status

project_config = dotenv_values(".env")
conn_str = project_config['CONECCTION']


client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
# TODO hide the name of the database. I tried diffent ways, but I can't seem use a variable to reference the database
database = client.ToBeDone
collection_users = database.Users
collection_tasks = database.Tasks


# USERS COLLECTION

async def username_exist(username:str):
    cursor = await collection_users.find_one({ "username": username})

    if cursor is None:
        return False
    else:
        return True



async def create_user(user):
    user["username"] = user["username"].lower()
    username_to_check = user["username"]

    user_already_exists = await username_exist(username_to_check) 

    if user_already_exists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"The username {username_to_check} already exists.")

    document = user
    # todo hash password
    result = await collection_users.insert_one(document)

    return document



async def fetch_all_users():    
    users = [] 
    cursor = collection_users.find({})
    async for document in cursor:
        users.append(Users(**document))

    return users


async def fetch_user_by_username(username):
    document = await collection_users.find_one({ "username": username})
    
    return document


async def update_user(username, full_name, email, disabled):
    current_info =  await fetch_user_by_username(username)

    updated_full_name = current_info["full_name"] if not full_name else full_name
    updated_email = current_info["email"] if not email else email
    if disabled is None:
        updated_disabled = current_info["disabled"]
    else:
        updated_disabled = disabled if not disabled == current_info["disabled"] else current_info["disabled"]    

    await collection_users.update_one(
        { "username": username},
        {"$set":{
            "full_name": updated_full_name,
            "email": updated_email,
            "disabled": updated_disabled
        }}
    )

    document = await collection_users.find_one({ "username": username})

    return document



async def remove_user(username):
    await collection_users.delete_one({ "username": username})

    return True
    



# TASKS COLLECTION
async def fetch_all_tasks():    
    tasks = [] 
    cursor = collection_tasks.find({})
    async for document in cursor:
        # this Task is the one defined at model.py
        tasks.append(Tasks(**document))

    return tasks


async def fetch_one_task(task):
    document = await collection_tasks.find_one({ "task": task})
    
    return document


async def create_task(task):
    document = task
    result = await collection_tasks.insert_one(document)

    return document


async def update_task(task, location):
    await collection_tasks.update_one({"task":task}, {"$set":{"location":location}})

    document = await collection_tasks.find_one({"task":task})

    return document


async def remove_task(task):
    await collection_tasks.delete_one({"task":task})

    return True


