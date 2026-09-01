import os

import uvicorn as uv
from fastapi import FastAPI as fapi

from main.main import router as main_router


app = fapi()

app.include_router(router=main_router)

@app.post("/status")
async def status():

    pass


if __name__ == "__main__":

    uv.run(
        app=app,
        host="0.0.0.0",
        port=int(os.getenv(key="PORT", default="8080"))
    )