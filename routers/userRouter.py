from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import get_db
from starlette import status


# from models import Users
from schemas import userSchema
from controllers import userController

router = APIRouter(
    prefix = '/users',
)


@router.get('/', response_model = list[userSchema.getUserInfoSchema])
def getUserList(db: Session = Depends(get_db)):
    userList = userController.getUserList(db)
    
    return userList

@router.post('/signup')
def createUser(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
    isExistEmail = userController.findUser(db, schema, False)
    if isExistEmail:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "email is Duplicated",
        )

    userController.createUser(db, schema)

    return {
        'status': 'success',
        'message': 'signup succeed'
    }

@router.post('/login')
def login(schema: userSchema.loginUserSchema, db: Session = Depends(get_db)):
    isExistUser = userController.findUser(db, schema, True)
    if isExistUser:
        user_uuid = isExistUser.user_id
        isTokenExists = userController.exists
        accessToken = userController.publishAccessToken(user_uuid)
        
        return {
            'status': 'success',
            'message': 'login succeed',
            'accessToken': accessToken,
        }
    else:
        return {
            'status': 'fail',
            'message': 'wrong email or password',
        }

@router.post('/logout')
def logout(request: Request):
    accessToken = request.headers.get('Authorization').replace('Bearer ', '')
    userController.revokeToken(accessToken)
    return {
        'status': 'success',
        'message': 'logout succeed'
    }