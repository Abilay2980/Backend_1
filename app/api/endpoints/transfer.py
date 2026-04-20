from fastapi import APIRouter,Depends,HTTPException
from app.db.database import db
from app.api.schemas.todo import Todo
from app.security.utils import ex_rate,transfer_money,change_balance
from datetime import datetime   
from app.security.dependencies import Permission_Checker,get_access
from app.api.schemas.transfer import Transfer

transfer_router = APIRouter(
    prefix="/transfer",
    tags=["Transfer"]
)


@transfer_router.get("/exchange_rate")
async def get_ex_rate():
    a = await ex_rate()
    return{"base_currency": "KZT","updated_at":datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S"),"rates":a}

@transfer_router.post("/transfer_money")
@Permission_Checker(["user"])
async def transfer(transfer:Transfer,payload :str = Depends(get_access)):
    res = await transfer_money(payload.get("sub"),transfer.name,transfer.amount)
    return{"detail":"Success","your_balance":res.get("balance")}


@transfer_router.post("/change_balance")
@Permission_Checker(["admin"])
async def change_balnce(transfer:Transfer,payload :str = Depends(get_access)):

    res = await change_balance(payload.get("sub"),transfer.name,transfer.amount)
    return{"detail":"success","new_balance":res.get("balance")}

        

