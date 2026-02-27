from fastapi import FastAPI
from pydantic import BaseModel
from cms_service import CMSService
import os
import socket
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="CMS Adapter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = CMSService(socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost"))+ ":" + str(8000))

service.register_cms_adapter(socket.gethostbyname(os.getenv("SERVICE_HOST", "localhost"))+ ":" + str(os.getenv("SERVICE_PORT", 8000)))

print("Hello, cms has started abcd")
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    return service.login(req.username, req.password)

@app.post("/new_order")
def new_order(order: dict):
    return service.new_order(order)

@app.get("/orders")
def view_orders():
    return service.view_orders()

@app.get("/orders/{order_id}")
def order_status(order_id: str):
    return service.order_status(order_id)

@app.get("/client_orders/{client_id}")
def client_orders(client_id: str):
    return service.client_orders(client_id)

@app.get("/bill/{order_id}")
def view_bill(order_id: str):
    return service.view_bill(order_id)