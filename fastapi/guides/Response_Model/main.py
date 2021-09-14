from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

# pip install email-validator
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# item model을 return하여 response로 줄 수 있음
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


# response와 input 모델을 다르게 주기
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# response_model_exclude_unset=True
# Model에 value를 주지 않으면 주지 않은대로 response

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

# include , exclude로 response 데이터 조작하기
# private한 데이터를 filter out 할 수 있음
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]
