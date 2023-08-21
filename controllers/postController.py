from models import Boards, Posts
from schemas import boardSchema
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import uuid
import jwt
import datetime

def checkAccessibleBoard(db: Session, boardID: int, userUUID: str):
    return db.query(Boards).filter(and_(Boards.board_id == boardID, or_(Boards.is_public == True, Boards.creator_id == userUUID))).first()

def getPostList(db: Session, boardID: int):
    return db.query(Posts).filter(Posts.board_id == boardID).all() # TODO: created_at 추가, pagination 추가