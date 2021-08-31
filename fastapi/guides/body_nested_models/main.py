from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []  # Set도 가능 : Set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Nested Model
# 이미지 모델을 만들어서
class Image(BaseModel):
    url: str  # str 대신에 pydantic에 HttpUrl로 변경 가능
    name: str


# 아이템 모델안으로 넣을 수 있음
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: Optional[List[Image]] = None  # List 가능


# Nest는 더 깊어 질 수 있음
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]  # <-


@app.post("/offers/")
async def create_offer(offer: offer):
    return offer
