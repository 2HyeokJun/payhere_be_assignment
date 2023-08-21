from fastapi import FastAPI
from routers import userRouter, boardRouter


app = FastAPI()
app.include_router(userRouter.router)
app.include_router(boardRouter.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}

