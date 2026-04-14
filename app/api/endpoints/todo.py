from fastapi import APIRouter


todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


@todo_router.get("/")
async def get_todos():
    pass


@todo_router.post("/")
async def create_todo():
    pass
