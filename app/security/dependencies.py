from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends

from datetime import datetime,timedelta
from app.core.config import settings
import jwt

oauth = OAuth2PasswordBearer("/login")
secret_word = settings.SECRET_WORD
algorithm="HS256"
access_token_time = 15 #minutes
refresh_token_time = 2 #days

def encode_token(data:dict):
    to_encode = data.copy()
    if data["type"] not in ["Access","Refresh"]:
        raise HTTPException(status_code=401,detail="Theres no such type of token")
    elif data["type"] == "Access":
        exp = datetime.utcnow()+timedelta(minutes=access_token_time)
    else:
        exp = datetime.utcnow()+timedelta(days = refresh_token_time)
    to_encode.update({"exp":exp})
    token = jwt.encode(to_encode,key=secret_word,algorithm=algorithm)
    return token
    
def decode_token(to_decode:str):
    try:
        payload = jwt.decode(to_decode,key = secret_word, algorithms=[algorithm])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=500,detail="expired signarute")
    raise HTTPException(status_code=400,detail="damaged token")
    
    
def get_access(token = Depends(oauth)):
    payload = decode_token(token)
    return payload

