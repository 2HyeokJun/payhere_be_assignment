from models import Boards
from schemas import boardSchema
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import uuid
import jwt
import datetime

def getBoardList(db: Session, userUUID: str):
    if userUUID is None:
        boardList = db.query(Boards).filter(Boards.is_public == True).order_by(desc(Boards.posts), desc(Boards.board_id)).all()
    else:
        boardList = db.query(Boards).filter(or_(Boards.is_public == True, Boards.creator_id == userUUID)).order_by(desc(Boards.posts), desc(Boards.board_id)).all()

    return boardList

def findBoard(db: Session, schema):
    return db.query(Boards).filter(Boards.board_name == schema.board_name).first()

def createBoard(db: Session, request_data: boardSchema.createBoardSchema, userUUID: str):
    createBoardQuery = Boards(
        board_name = request_data.board_name,
        is_public = request_data.is_public,
        creator_id = userUUID,
    )
    db.add(createBoardQuery)
    db.commit()