# MongoDB Driver
import motor.motor_asyncio
from model import (
    Tasks, Users,
)
from dotenv import dotenv_values


project_config = dotenv_values(".env")
conn_str = project_config['CONECCTION']


client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
# TODO hide the name of the database. I tried diffent ways, but I can't seem use a variable to reference the database
database = client.ToBeDone
collection_users = database.Users
collection_tasks = database.Tasks


# USERS COLLECTION
async def create_user(user):
    document = user
    result = await collection_users.insert_one(document)

    return document


async def fetch_all_users():    
    users = [] 
    cursor = collection_users.find({})
    async for document in cursor:
        # this Task is the one defined at model.py
        users.append(Users(**document))

    return users


async def fetch_user_by_username(username):
    document = await collection_users.find_one({ "username": username})
    
    return document

# todo update this method to receive a user document, and just upd what id not None, so I don't overwrite data
# todo add optional fields
async def update_user(username, full_name, email, hashed_password, disabled):
    await collection_users.update_one(
        { "username": username},
        {"$set":{
            "full_name": full_name,
            "email": email,
            "hashed_password": hashed_password,
            "disabled":disabled
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


