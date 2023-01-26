from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pymongo import MongoClient
from typing import List,Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn
import requests

app = FastAPI()



# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017')
db = client['airworks']
collection = db['users']

class User(BaseModel):
    username: str
    password: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}
    
@app.post("/signup")
async def signup(user: User):
    db = client["airworks"]
    existing_user = db.users.find_one({"username": user.username})
    if existing_user is not None:
        return {"message": "Username already taken"}
    db.users.insert_one({"company name": user.username, "industry": user.industry, "company email": user.email,"password": user.password})
    return {"message": "Successfully registered"}
    
@app.post("/login")
async def login(user: User):
    db = client["airworks"]
    existing_user = db.users.find_one({"username": user.username})
    if existing_user is not None:
        return {"message": "valid username or password"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)

