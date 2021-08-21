from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# id 별 수정
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# 선언한 모델에 직접 접근 가능
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item_tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
