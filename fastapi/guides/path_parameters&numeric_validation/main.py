from typing import Optional
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item_query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Path, Query에 ge, le 등 인자를 줘서 숫자 범위를 정해줄 수 있음
