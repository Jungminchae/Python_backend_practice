from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# pydantic schema_extra
# example schema
# 1
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None


#     class Config:
#         schema_extra = {
#             "example" : {
#                 "name" : "foo",
#                 "description" : "A very nice Item",
#                 "price" : 35.4,
#                 "tax" : 3.2,
#             }
#         }

# 2
class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# 인자값에 Body(..., example={ name: "Foo" ... }) 가능
