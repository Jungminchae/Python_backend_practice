from fastapi import FastAPI

# 시작이 Flask와 매우 닮은것 같다
app = FastAPI()

# endpoint get method
@app.get("/")
async def root():
    return {"message": "Hello World"}
