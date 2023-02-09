from fastapi import FastAPI
import pandas as pd


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
