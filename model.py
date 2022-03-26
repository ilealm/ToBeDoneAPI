# pydantic helps to autocreate the json schema from the model
# All the data validation is performed under the hood by Pydantic (e.g /docs)
from pydantic import BaseModel, EmailStr
# maybe letter I will nedd this
from typing import Optional
# from typing import List, Optional



    
class Tasks(BaseModel):
    task: str
    location: str


class Users(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    disabled: Optional[bool] = False



    # "username": "johndoe",
    # "full_name": "John Doe",
    # "email": "johndoe@example.com",
    # "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    # "disabled": False,

#     fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }