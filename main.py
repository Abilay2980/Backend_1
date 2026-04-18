import uvicorn
from fastapi import FastAPI,Depends,HTTPException
from contextlib import asynccontextmanager
from app.api.endpoints.todo import todo_router
from app.db.database import db
from app.security.utils import verify_password,hash_password
from app.security.dependencies import decode_token,encode_token,get_access,get_roles,get_user
from app.api.schemas.security import User_login,User_db
from app.api.endpoints.transfer import transfer_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await db.connect()
    yield
    await db.disconnect()



app = FastAPI(lifespan=lifespan)

app.include_router(todo_router)
app.include_router(transfer_router)

@app.post("/register")
async def register(user:User_login):
    a = await db.fetch("select username from users join users_roles using(user_Id) join roles using(role_id) where username = $1",user.username)
    if a:
        raise HTTPException(status_code=401,detail="This name is already taken")
    hashed_pass = hash_password(user.password)
    await db.execute("with num1 as (insert into users(username,password) values($1,$2) returning user_id),num2 as (SELECT role_id FROM roles WHERE role = 'user') insert into users_roles(user_id,role_id) select num1.user_id,num2.role_id from num1,num2",user.username,hashed_pass)
    return {"detail":"New user has been created"}

@app.post("/login")
async def login(user:User_login):
    a = await db.fetch("select username,password from users join users_roles using(user_Id) join roles using(role_id) where username = $1",user.username)
    if not a:
        raise HTTPException(status_code=401, detail="Wrong password")
    credents = User_db(username = a[0]["username"],hashed_password = a[0]["password"])
    if verify_password(user.password,credents.hashed_password):
        token = encode_token({"sub":user.username,"type":"Access"})
    else:
        raise HTTPException(status_code=401, detail="Wrong password")
    return token

@app.get("/info")
async def get_info(payload:str = Depends(get_access)):
    return{"Username":payload["sub"],"Roles":await get_roles(payload["sub"])}

        
    
    
    








if __name__ == "__main__":
    uvicorn.run(app="main:app",reload =True)