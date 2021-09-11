from typing import Optional
from fastapi import FastAPI, Cookie

app = FastAPI()


@app.get("/items/")
async def read_times(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


# Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class.
# But remember that when you import Query, Path, Cookie and others from fastapi, those are actually functions that return special classes.
