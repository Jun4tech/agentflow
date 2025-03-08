from fastapi import FastAPI
from agents.routes import router


app = FastAPI(
    title="AIDA",
    description="Welcome to AIDA's API documentation, here you can interact with your Assistance.",
)

app.include_router(router)