from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
# from starlette import status
from models.users import Users


from schemas import userSchema
# from controllers import userController

router = APIRouter(
    prefix = '/users',
)

@router.post('/signup')
def signUp(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
    newUser = Users(db)
    signUpResult = newUser.enroll(schema)
    print('signUpResult:', signUpResult)
    return signUpResult

@router.post('/login')
def logIn(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
    logInUser = Users(db)
    print('schema;', schema)
    loginResult = logInUser.login(schema)
    return loginResult

# @router.post('/logout')
# def logout(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):


# def createUser(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
#     isExistEmail = userController.findUser(db, schema, checkPassword = False)
#     if isExistEmail:
#         raise HTTPException(
#             status_code = status.HTTP_409_CONFLICT,
#             detail = "email is Duplicated",
#         )

#     userController.createUser(db, schema)

#     return {
#         'status': 'success',
#         'message': 'signup succeed'
#     }

# @router.post('/login')
# def login(schema: userSchema.loginUserSchema, db: Session = Depends(get_db)):
#     isExistUser = userController.findUser(db, schema, checkPassword = True)
#     if isExistUser:
#         userUUID = isExistUser.user_uuid
#         accessToken = userController.publishAccessToken(userUUID)
        
#         return {
#             'status': 'success',
#             'message': 'login succeed',
#             'accessToken': accessToken,
#         }
#     else:
#         return {
#             'status': 'fail',
#             'message': 'wrong email or password',
#         }

# @router.post('/logout')
# def logout(request: Request):
#     userUUID = verifyToken(request, softVerify = False)
#     userController.deleteFromRedis(userUUID)
#     return {
#         'status': 'success',
#         'message': 'logout succeed'
#     }