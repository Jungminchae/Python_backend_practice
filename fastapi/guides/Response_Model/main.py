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
