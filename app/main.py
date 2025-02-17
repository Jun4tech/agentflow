from fastapi import FastAPI
from llm import main

app = FastAPI()

@app.get("/")
async def root():
    return main()