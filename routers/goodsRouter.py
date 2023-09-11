from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
# from starlette import status
from models.goods import Goods
from schemas import goodSchema
import os

router = APIRouter(
    prefix = '/goods',
)

@router.post('/create')
def createGoods(schema: goodSchema.createGoodSchema, db: Session = Depends(get_db)):
    newGoods = Goods(db)
    createResult = newGoods.create(schema)
    return createResult

@router.get('/list')
def seeGoodsList(cursor: int, db: Session = Depends(get_db)):
    selectedGoods = Goods(db)
    listResult = selectedGoods.list_view(cursor)
    return listResult




@router.get('/{goodsID}')
def seeGoodsDetail(goodsID: int, db: Session = Depends(get_db)):
    selectedGoods = Goods(db)
    detailResult = selectedGoods.detail_view(goodsID)
    return detailResult

@router.put('/{goodsID}')
def modifyGoods(goodsID: int, schema: goodSchema.createGoodSchema, db: Session = Depends(get_db)):
    selectedGoods = Goods(db)
    modifyResult = selectedGoods.modify(goodsID, schema)
    return modifyResult

@router.delete('/{goodsID}')
def modifyGoods(goodsID: int, db: Session = Depends(get_db)):
    selectedGoods = Goods(db)
    deleteResult = selectedGoods.delete(goodsID)
    return deleteResult