from fastapi import FastAPI

app = FastAPI()

# parameter 타입을 지정할 수 있음
# 타입을 지정했을 때 그 타입이 아니면 에러
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 경로 동작은 순차적으로 평가
# 나를 나타내는 경우를 고려하여 read_user_me를 read_user보다 먼저 선언
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "현재 유저"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# 유효하고 미리 정의할 수 있는 경로 매개변수 값을 원한다면 파이썬 표준 Enum을 사용할 수 있습
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    # .value로 값을 가져올 수 있음 -> str
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# 경로를 포함하는 경로 parameter
# :path를 써서 구분


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
