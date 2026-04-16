from fastapi import APIRouter
from app.db.database import db
from app.api.schemas.todo import Todo
from app.security.utils import ex_rate
from datetime import datetime   

transfer_router = APIRouter(
    prefix="/transfer",
    tags=["Transfer"]
)


@transfer_router.get("/exchange_rate")
async def get_ex_rate():
    a = await ex_rate()
    return{"base_currency": "KZT","updated_at":datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S"),"rates":a}



