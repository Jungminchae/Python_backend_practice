from typing import Optional, List
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


# convert_underscore를 False로 설정하기 전에, 어떤 HTTP 프록시들과 서버들은 언더스코어가 포함된 헤더 사용을 허락하지 않는다는 것을 명심하십시오.
@app.get("/items/")
async def read_item(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# 중복 헤더가 나올 때
@app.get("/items/")
async def read_item(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}


# {
#     "X-Token values": [
#         "bar",
#         "foo"
#     ]
# }
