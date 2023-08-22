from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware import verifyToken, checkIsAccessibleBoard
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
def getPostList(boardID: int, request: Request, db: Session = Depends(get_db), page: int = 1, isAccessible: bool = Depends(checkIsAccessibleBoard)):
    postList = postController.getPostList(db, boardID, page)

    return postList

@router.post('/{boardID}')
def createPost(request: Request, boardID: int, schema: postSchema.createPostSchema, db: Session = Depends(get_db), isAccessible: bool = Depends(checkIsAccessibleBoard)):
    checkIsAccessibleBoard(request, boardID, db)
    userUUID = verifyToken(request, softVerify = False)
    postController.createPost(db, schema, boardID, userUUID)

    return {
        'status': 'success',
        'message': 'post creation succeed',
    }

@router.put('/{boardID}/{postID}')
def updatePost(request: Request, postID: int, schema: postSchema.createPostSchema, db: Session = Depends(get_db), isAccessible: bool = Depends(checkIsAccessibleBoard)):
    userUUID = verifyToken(request, softVerify = False)
    updateResult = postController.updatePost(db, schema, postID, userUUID)
    if not updateResult:
        raise HTTPException(status_code = 400, detail = "wrong post_id")

    return {
        'status': 'success',
        'message': 'post update succeed',
    }

@router.delete('/{boardID}/{postID}')
def deletePost(request: Request, boardID: int, postID: int, db: Session = Depends(get_db), isAccessible: bool = Depends(checkIsAccessibleBoard)):
    userUUID = verifyToken(request, softVerify = False)
    deleteResult = postController.deletePost(db, boardID, postID, userUUID)
    if not deleteResult:
        raise HTTPException(status_code = 400, detail = "wrong post_id")

    return {
        'status': 'success',
        'message': 'post delete succeed',
    }
