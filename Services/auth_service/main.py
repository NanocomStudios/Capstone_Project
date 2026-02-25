from fastapi import FastAPI
from pydantic import BaseModel
import requests
import socket
import os
import hashlib
import time

import sqlite3

from fastapi.middleware.cors import CORSMiddleware

conn = sqlite3.connect('users.db')

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, username TEXT, FOREIGN KEY(username) REFERENCES users(username))")

c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('bhanuka', '123', 'client')")
conn.commit()
conn.close()

def register_on_service_reg():
    registry = socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost")) + ":" + str(8000)
    service = socket.gethostbyname(os.getenv("SERVICE_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_PORT", 8006))

    req = {"name":"auth-service","address" : str(service)}
    r = requests.post("http://" + registry + "/register", json=req)
    if(r.status_code == 200):
        print("Registered on the service registery")
        return True
    else:
        print("Failed to register on the service registery")
        return False

if(register_on_service_reg() != True):
    exit(-1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str

class Session(BaseModel):
    username: str
    sessionID: str

class NewUser(BaseModel):
    username: str
    password: str
    role: str

@app.post("/login")
def login(user: User):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = c.fetchone()
    if result:
        session_id = hashlib.sha256((user.username + user.password + str(time.time())).encode()).hexdigest()
        c.execute("INSERT OR REPLACE INTO sessions (session_id, username) VALUES (?, ?)", (session_id, user.username))
        conn.commit()
        conn.close()
        return {"response": "success", "sessionID" : session_id}
    else:
        conn.close()
        return {"response": "failure"}
    

@app.post("/get_role")
def get_role(session : Session):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT role FROM sessions LEFT JOIN users ON sessions.username = users.username WHERE sessions.session_id=? AND sessions.username=?", (session.sessionID,session.username))
    result = c.fetchone()
    conn.close()
    if result:
        return {"role" : result[0]}
    else:
        return {"role" : "none"}
    
@app.post("/register")
def register(user: NewUser):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (user.username, user.password, user.role))
        conn.commit()
        conn.close()
        return {"response": "success"}
    except sqlite3.IntegrityError:
        conn.close()
        return {"response": "failure", "error": "Username already exists"}
    
@app.get("/health")
def health():
    return {"status": "healthy"}