# middleware.py

from fastapi import Request, HTTPException
from dotenv import load_dotenv
import jwt
import os

load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')

def verifyToken(request: Request, softVerify: bool = False):
    if not request.headers.get('Authorization'):
        if softVerify:
            return None
        else:
            raise HTTPException(status_code = 401, detail = "Do not have token")
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(token, secretKey, algorithms=["HS256"])
        userUUID = payload.get('userUUID')
        return userUUID
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code = 401, detail = "Cannot decode token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")
