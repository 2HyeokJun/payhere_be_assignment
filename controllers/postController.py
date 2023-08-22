from models import Boards, Posts
from schemas import postSchema
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import uuid
import jwt
import datetime
# TODO: userUUID 모든 조건에 넣었는지 확인

def checkAccessibleBoard(db: Session, boardID: int, userUUID: str):
    return db.query(Boards).filter(and_(Boards.board_id == boardID, or_(Boards.is_public == True, Boards.creator_id == userUUID))).first()

def getPostList(db: Session, boardID: int):
    return db.query(Posts).filter(Posts.board_id == boardID).all() # TODO: created_at 추가, pagination 추가

def createPost(db: Session, request_data: postSchema.createPostSchema, boardID: int, userUUID: str):
    createPostQuery = Posts(
        board_id = boardID,
        post_title = request_data.post_title,
        post_content = request_data.post_content,
        creator_id = userUUID,
    )
    db.add(createPostQuery)
    boardObject = db.query(Boards).filter(Boards.board_id == boardID).first()
    boardObject.posts += 1
    db.commit()

def updatePost(db: Session, request_data: postSchema.createPostSchema, postID: int, userUUID: str):
    selectedPost = db.query(Posts).filter(and_(Posts.post_id == postID, Posts.creator_id == userUUID)).first()
    selectedPost.post_title = request_data.post_title
    selectedPost.post_content = request_data.post_content
    db.commit()

def deletePost(db: Session, boardID: int, postID: int, userUUID: str):
    selectedPost = db.query(Posts).filter(and_(Posts.post_id == postID, Posts.creator_id == userUUID)).first()
    db.delete(selectedPost)
    boardObject = db.query(Boards).filter(Boards.board_id == boardID).first()
    boardObject.posts -= 1
    db.commit()