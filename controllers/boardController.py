from models import Boards
from schemas import boardSchema
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session

pageLimit = 10

def getBoardList(db: Session, userUUID: str, page: int):
    offset = (page - 1) * pageLimit
    if userUUID is None:
        boardList = db.query(Boards).filter(Boards.is_public == True).order_by(desc(Boards.posts), desc(Boards.board_id)).offset(offset).limit(pageLimit).all()
    else:
        boardList = db.query(Boards).filter(or_(Boards.is_public == True, Boards.creator_id == userUUID)).order_by(desc(Boards.posts), desc(Boards.board_id)).offset(offset).limit(pageLimit).all()

    return boardList

def findBoard(db: Session, schema):
    return db.query(Boards).filter(Boards.board_name == schema.board_name).first()

def checkAccessibleBoard(db: Session, boardID: int, userUUID: str):
    return db.query(Boards).filter(and_(Boards.board_id == boardID, or_(Boards.is_public == True, Boards.creator_id == userUUID))).first()
        
def checkIsMyBoard(db: Session, boardID: int, userUUID: str):
    return db.query(Boards).filter(and_(Boards.board_id == boardID, Boards.creator_id == userUUID)).first()

def createBoard(db: Session, request_data: boardSchema.createBoardSchema, userUUID: str):
    createBoardQuery = Boards(
        board_name = request_data.board_name,
        is_public = request_data.is_public,
        creator_id = userUUID,
    )
    db.add(createBoardQuery)
    db.commit()

def updateBoard(db: Session, request_data: boardSchema.createBoardSchema, boardID: int):
    selectedBoard = db.query(Boards).filter(Boards.board_id == boardID).first()
    selectedBoard.board_name = request_data.board_name
    selectedBoard.is_public = request_data.is_public
    db.commit()

def deleteBoard(db: Session, boardID: int):
    selectedBoard = db.query(Boards).filter(Boards.board_id == boardID).first()
    db.delete(selectedBoard)
    db.commit()