from models import Boards, Posts
from schemas import postSchema
from sqlalchemy import and_
from sqlalchemy.orm import Session

pageLimit = 10

def getPostList(db: Session, boardID: int, page: int):
    offset = (page - 1) * pageLimit
    return db.query(Posts).filter(Posts.board_id == boardID).offset(offset).limit(pageLimit).all()

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