from fastapi import FastAPI
from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "STT Server is running."}