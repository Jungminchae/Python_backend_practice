from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI()

# @app.get("/items/")
# async def read_items(q: Optional[str]=None):
#     results = {"items" : [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# additional validation
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, max_length=50)
):  # min_length=3, regex="^fixedquery$" 등 다른 매개변수도 넣을 수 있음
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query(..., min_length=3) 처럼 사용하여 required하게 만들 수 있음, ...은 파이썬 Ellipsis
# q: Optional(List[str] = Query(None)) 으로 주고 q를 리스트 형태로 여러개 원소를 가진 녀석으로 받을 수 있음, /items/?q=blah&q=blah2
# 그냥 Query([]) 를 바로 넣을 수 있고 그 안에 값을 기본값을 줄 수도 있음
# q : Optional[str] = Query(ailias =blahblah) alias를 줄 수도 있음
