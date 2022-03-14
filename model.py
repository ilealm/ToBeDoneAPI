# pydantic helps to autocreate the json schema from the model
# All the data validation is performed under the hood by Pydantic (e.g /docs)
from pydantic import BaseModel
# maybe letter I will nedd this
# from typing import List, Optional

    
class Tasks(BaseModel):
    task: str
    location: str
