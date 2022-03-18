# MongoDB Driver
import motor.motor_asyncio
from model import Tasks
from dotenv import dotenv_values


project_config = dotenv_values(".env")
conn_str = project_config['CONECCTION']



client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
# TODO hide the name of the database. I tried diffent ways, but I can't seem use a variable to reference the database
database = client.ToBeDone
collection = database.Tasks



async def fetch_all_tasks():
    
    tasks = [] 
    cursor = collection.find({})
    async for document in cursor:
        # this Task is the one defined at model.py
        tasks.append(Tasks(**document))

    return tasks


async def fetch_one_task(task):
    document = await collection.find_one({ "task": task})
    
    return document


async def create_task(task):
    document = task
    result = await collection.insert_one(document)

    return document


async def update_task(task, location):
    await collection.update_one({"task":task}, {"$set":{"location":location}})

    document = await collection.find_one({"task":task})

    return document

async def remove_task(task):
    await collection.delete_one({"task":task})

    return True