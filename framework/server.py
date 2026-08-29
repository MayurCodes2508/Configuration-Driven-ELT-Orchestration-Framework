import os

import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.post("/execute")
async def execute():

    return {
        "msg": "Test_1",
        "status": "SUCCESS"
    }


if __name__ == "__main__":

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(os.getenv(key="PORT", default="8080"))
    )