from pydantic import BaseModel
from datetime import datetime
class Todo(BaseModel):
    description:str
    completed:bool

