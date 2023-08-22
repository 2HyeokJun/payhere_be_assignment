from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from starlette import status


# from models import Users
from schemas import userSchema
from controllers import userController
from middleware import verifyToken

router = APIRouter(
    prefix = '/users',
)


@router.get('/', response_model = list[userSchema.getUserInfoSchema])
def getUserList(db: Session = Depends(get_db)):
    userList = userController.getUserList(db)
    
    return userList

@router.post('/signup')
def createUser(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
    isExistEmail = userController.findUser(db, schema, checkPassword = False)
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
    isExistUser = userController.findUser(db, schema, checkPassword = True)
    if isExistUser:
        userUUID = isExistUser.user_uuid
        accessToken = userController.publishAccessToken(userUUID)
        
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
    userUUID = verifyToken(request, softVerify = False)
    userController.deleteFromRedis(userUUID)
    return {
        'status': 'success',
        'message': 'logout succeed'
    }