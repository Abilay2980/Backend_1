from passlib.context import CryptContext
from app.security.dependencies import get_access
from fastapi import Depends 
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

async def get_user(payload : str = Depends(get_access)):
    a = await db.fetch("select username,password from users join users_roles using(user_Id) join roles using(role_id) where username = $1",payload["sub"])
    return User_db(username=a["username"],hash_password=a["password"])
    
async def get_roles(sub:str):
    a = await db.fetch("select role from users join users_roles using(user_Id) join roles using(role_id) where username = $1",sub)
    a = [i["role"] for i in a]
    return a
    

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



