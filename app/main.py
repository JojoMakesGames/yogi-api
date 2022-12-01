from fastapi import FastAPI
from app.schema import graphql_app
import uvicorn

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)