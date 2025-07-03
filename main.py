from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"FastAPI": "0.1.0"}}


@app.get("/about")
def about():
    return {"data": {"FastAPI": "0.1.0"}, "description": "A simple FastAPI application."}


