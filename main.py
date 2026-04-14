import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints.todo import todo_router
from app.db.database import db

@asynccontextmanager
async def lifespan(app:FastAPI):
    await db.connect()
    yield
    await db.disconnect()



app = FastAPI(lifespan=lifespan)

app.include_router(todo_router)


@app.get("/")
async def info():
    res = await db.fetch("select * from todo")
    return{"detail":res}

if __name__ == "__main__":
    uvicorn.run(app="main:app",reload =True)