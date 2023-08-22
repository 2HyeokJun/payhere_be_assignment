from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from starlette import status
from middleware import verifyToken
from dotenv import load_dotenv
import os

from schemas import postSchema
from controllers import postController
load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')

router = APIRouter(
    prefix = '/posts',
)

@router.get('/{boardID}', response_model = list[postSchema.getPostInfoSchema])
def getPostList(boardID: int, request: Request, db: Session = Depends(get_db), page: int = 1):
    userUUID = verifyToken(request, softVerify = False)
    isAccessibleBoard = postController.checkAccessibleBoard(db, boardID, userUUID)
    
    if not isAccessibleBoard:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized to access that board",
        )
    
    postList = postController.getPostList(db, boardID, page)

    return postList

@router.post('/{boardID}')
def createPost(request: Request, boardID: int, schema: postSchema.createPostSchema, db: Session = Depends(get_db)):
    userUUID = verifyToken(request, softVerify = False)
    postController.createPost(db, schema, boardID, userUUID)

    return {
        'status': 'success',
        'message': 'post creation succeed',
    }

@router.put('/{boardID}/{postID}')
def updatePost(request: Request, postID: int, schema: postSchema.createPostSchema, db: Session = Depends(get_db)):
    userUUID = verifyToken(request, softVerify = False)
    postController.updatePost(db, schema, postID, userUUID)

    return {
        'status': 'success',
        'message': 'post update succeed',
    }

@router.delete('/{boardID}/{postID}')
def deletePost(request: Request, boardID: int, postID: int, db: Session = Depends(get_db)):
    userUUID = verifyToken(request, softVerify = False)
    postController.deletePost(db, boardID, postID, userUUID)

    return {
        'status': 'success',
        'message': 'post delete succeed',
    }
