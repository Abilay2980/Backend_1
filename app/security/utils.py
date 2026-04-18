from passlib.context import CryptContext
from app.security.dependencies import get_access
from fastapi import Depends ,HTTPException
from app.api.schemas.security import User_db
from bs4 import BeautifulSoup
import requests
from decimal import Decimal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

from app.db.database import db


async def ex_rate():
    url = "https://www.mig.kz/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.find_all("td")
    allNews = [i.text for i in allNews if len(i.text.strip())>2 and i.text != "по курсу"]
    new = []
    for i in range(0,len(allNews),3):
        new.append({"currency":allNews[i+1],"sell":Decimal(allNews[i]),"buy":Decimal(allNews[i+2])})
    return new

async def transfer_money(sender:str,receiver:str,amount:Decimal):
    async with db.transaction(isolation='serializable'):
        try:
            if sender == receiver:
                raise HTTPException(status_code=400,detail="Bad request")
            res = await db.fetch("select balance from users join users_balances using(user_id) where username = $1",sender)
            if res[0]["balance"] < amount:
                raise HTTPException(status_code=400,detail="Not enough funds")
            res = await db.fetch("update users_balances set balance= balance -$1 where user_id = (select user_id from users where username = $2) returning balance",amount,sender)
            await db.execute("update users_balances set balance=balance+$1 where user_id = (select user_id from users where username = $2)",amount,receiver)
            return{"detail":"success","sender new balance":res}
        except Exception as e:
            raise HTTPException(status_code=400,detail="Bad request")

async def change_balance(receiver:str,amount:Decimal):
    try:
        bal = await db.fetch("update users_balances set balance = $1 where user_id = (select user_id from  users where username = $2) returning balance",amount,receiver)
        return{"detail":"success","bal":bal[0]["balance"]}
    except Exception as e:
        return{"detail":str(e)}
        raise HTTPException(status_code=400,detail="Bad Request")
    

            
        

        





