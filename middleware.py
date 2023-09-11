from fastapi import Request, Depends, HTTPException
from dotenv import load_dotenv
from starlette import status

import jwt
import os
from database import get_db, redisClient
from controllers import boardController

load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')

def verifyToken(request: Request):
    if not request.headers.get('Authorization'):
        raise HTTPException(status_code = 401, detail = "Do not have token")
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(token, secretKey, algorithms=["HS256"])
        userUUID = payload.get('userUUID')
        tokenInRedis = redisClient.get(userUUID)
        if token != tokenInRedis:
            raise HTTPException(status_code = 401, detail = "You are logged out")
        return userUUID
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code = 401, detail = "Cannot decode token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")