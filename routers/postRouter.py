from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from starlette import status
from middleware import verifyToken
from dotenv import load_dotenv
import jwt
import os

from schemas import postSchema
from controllers import postController
load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')

router = APIRouter(
    prefix = '/posts',
)
# TODO: boardRouter와 통합해서 하나로 묶기
def getUUIDOrNoneFromToken(accessToken: str):
    try:
        payload = jwt.decode(accessToken, secretKey, algorithms=["HS256"])
        userUUID = payload.get('userUUID')
        return userUUID
    except:
        return None

@router.get('/{boardID}', response_model = list[postSchema.getPostInfoSchema])
def getPostList(boardID: int, request: Request, db: Session = Depends(get_db)):
    if not request.headers.get('Authorization'):
        userUUID = None
    else:
        userUUID = getUUIDOrNoneFromToken(request.headers.get('Authorization').replace('Bearer ', ''))
    isAccessibleBoard = postController.checkAccessibleBoard(db, boardID, userUUID)
    
    if not isAccessibleBoard:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized to access that board",
        )
    
    postList = postController.getPostList(db, boardID)

    return postList
    
    
    