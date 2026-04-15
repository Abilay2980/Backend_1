from passlib.context import CryptContext
from app.security.dependencies import get_access
from fastapi import Depends 
from app.api.schemas.security import User_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

def get_user(sub : str = Depends(get_access)):
    from db.database import db
    a = db.fetch("select username,password from users join users_roles using(user_Id) join roles using(role_id) where username = $1",sub)
    return User_db(a["username"],a["password"])
    



    

