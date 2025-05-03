from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users/")
def read_users():
    return {"message": "List of users"}

@app.post("/users/")
def create_user():
    return {"message": "User created"}