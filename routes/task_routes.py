from fastapi import HTTPException, status
from main import app
# IMPORTANT In order to use the response_model=, I need to import the model
from model import Tasks


from database import(
    fetch_one_task,
    fetch_all_tasks,
    create_task, 
    update_task,
    remove_task,
)


@app.get("/api/tasks/")
async def get_tasks():
    response = await fetch_all_tasks()
    return response


@app.get("/api/task/{task}", response_model=Tasks)
async def get_task_by_task(task):
    response = await fetch_one_task(task)

    if response:
        return response
    raise HTTPException(404, f"There is no task with the name {task}.")


# TODO add the rest of status
# response_model=Task and :Task is to say I want the task to be as my model Task
@app.post("/api/task", response_model=Tasks, status_code=status.HTTP_201_CREATED)
async def post_task(task:Tasks):
    # create task is waiting for a JSON, that's why I'm using .dict
    response = await create_task(task.dict())

    if response:
        return response    
    raise HTTPException(400, "Something when wrong / bad request.")


@app.put("/api/task/{task}", response_model=Tasks)
async def put_task(task:str, location:str):
    response = await update_task(task, location)

    if response:
        return response    
    raise HTTPException(404, detail= f"There is no task with the name {task}")



@app.delete("/api/task/{task}")
async def delete_task(task):
    response = await remove_task(task)

    if response:
        return "Task succesfully deleted."
    
    raise HTTPException(404, f"Task not found {task}")