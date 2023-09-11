from models.sqlalchemy_schemas import GoodSchema
from schemas import goodSchema
from sqlalchemy.orm import Session
import os

class Goods:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schema: goodSchema.createGoodSchema):
        def extract_first_consonant(name):
            chosung_list = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"] 
            result = "" 
            for character in name: 
                code = ord(character) - 44032
                if code > -1 and code < 11172: 
                    result += chosung_list[code // 588]
                else: result += character
            return result
        
        schema.first_consonant = extract_first_consonant(schema.name)
        schema.creator_id = '61408d63-f3d8-42e9-b4eb-184e140dade9'
        print('schema:', schema)
        goods = GoodSchema(**schema.dict())
            
        print('goods:', goods)
        self.db.add(goods)
        self.db.commit()
        return {
            id: goods.goods_id,
        }

    def list_view(self, cursor: int, name = None):
        page_limit = os.environ.get('PAGE_LIMIT')
        if name is None:
            goods = self.db.query(GoodSchema).offset(cursor).limit(page_limit).all()
        else:
            goods = self.db.query(GoodSchema).filter(GoodSchema.name.like(f'%{name}%')).offset(cursor).limit(page_limit).all()
        return goods

    def detail_view(self, goodsID: int):
        selectedGoods = self.db.query(GoodSchema).filter(GoodSchema.goods_id == goodsID).first()
        return selectedGoods

    def modify(self, goodsID: int, schema: goodSchema.createGoodSchema):
        selectedGoods = self.db.query(GoodSchema).filter(GoodSchema.goods_id == goodsID).first()
        if not selectedGoods:
            raise ValueError #TODO:
        print('schema:', schema)
        selectedGoods = GoodSchema(**schema.dict())
        print('updated:', selectedGoods.name)
        self.db.commit()
        return 'success'

    def delete(self, goodsID: int):
        selectedGoods = self.db.query(GoodSchema).filter(GoodSchema.goods_id == goodsID).first()
        if not selectedGoods:
            raise ValueError #TODO:
        self.db.delete(selectedGoods)
        self.db.commit()
        return 'success'