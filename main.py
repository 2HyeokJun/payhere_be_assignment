from fastapi import FastAPI
from routers import userRouter, goodsRouter

app = FastAPI()
app.include_router(userRouter.router)
app.include_router(goodsRouter.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}

