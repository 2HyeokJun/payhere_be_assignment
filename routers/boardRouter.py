from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from starlette import status
from middleware import verifyToken
from dotenv import load_dotenv
import jwt
import os

from schemas import boardSchema
from controllers import boardController

load_dotenv()

secretKey = os.environ.get('JWT_SECRET_KEY')



router = APIRouter(
    prefix = '/boards',
)

def getUUIDOrNoneFromToken(accessToken: str):
    try:
        payload = jwt.decode(accessToken, secretKey, algorithms=["HS256"])
        userUUID = payload.get('userUUID')
        return userUUID
    except:
        return None
    
@router.get('/', response_model = list[boardSchema.getBoardInfoSchema])
def getBoardList(request: Request, db: Session = Depends(get_db)):
    if not request.headers.get('Authorization'):
        userUUID = None
    else:
        userUUID = getUUIDOrNoneFromToken(request.headers.get('Authorization').replace('Bearer ', ''))

    boardList = boardController.getBoardList(db, userUUID)
    
    return boardList

@router.post('/')
def createBoard(schema: boardSchema.createBoardSchema, db: Session = Depends(get_db), userUUID: str = Depends(verifyToken)):
    isExistBoard = boardController.findBoard(db, schema)
    if isExistBoard:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "board_name is Duplicated",
        )

    boardController.createBoard(db, schema, userUUID)

    return {
        'status': 'success',
        'message': 'board creation succeed',
    }

# TODO: isMyBoard 하나로 처리
@router.put('/{boardID}')
def updateBoard(boardID: int, schema: boardSchema.createBoardSchema, db: Session = Depends(get_db), userUUID: str = Depends(verifyToken)):
    isMyBoard = boardController.checkAuthorizedBoard(db, boardID, userUUID)
    if not isMyBoard:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized to access that board",
        )

    isExistBoard = boardController.findBoard(db, schema)
    if isExistBoard:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "board_name is Duplicated",
        )

    boardController.updateBoard(db, schema, boardID)

    return {
        'status': 'success',
        'message': 'board update succeed',
    }

# TODO: soft delete 고려: isMyBoard에 접근할때 not authorized인지 삭제된 게시판인지 구분할 필요가...있나?
@router.delete('/{boardID}')
def deleteBoard(boardID: int, db: Session = Depends(get_db), userUUID: str = Depends(verifyToken)):
    isMyBoard = boardController.checkAuthorizedBoard(db, boardID, userUUID)
    if not isMyBoard:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized to access that board",
        )
    boardController.deleteBoard(db, boardID)

    return {
        'status': 'success',
        'message': 'board delete succeed',
    }