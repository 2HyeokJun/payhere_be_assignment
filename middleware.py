# middleware.py

from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

# 미들웨어 함수 작성
def verifyToken(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secretKey, algorithms=["HS256"])
        userUUID = payload.get('userUUID')
        return userUUID
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code = 401, detail = "Cannot decode token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")
