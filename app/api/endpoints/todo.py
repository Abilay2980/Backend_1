from fastapi import APIRouter
from app.db.database import db
from app.api.schemas.todo import Todo

todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


@todo_router.get("/")
async def get_todos():
    res = await db.fetch("select * from todo ")
    return{"detail":res}
    pass


@todo_router.post("/")
async def create_todo(ex:Todo):
    await db.fetch("insert into todo(description,completed) values($1,$2)",ex.description,ex.completed)
    return {"detail":"Success"}
