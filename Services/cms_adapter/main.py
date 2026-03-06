from fastapi import FastAPI
from pydantic import BaseModel
from cms_service import CMSService
from threading import Thread
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Lib.publisher import consume
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

def cms_new_order_listener():
    def callback(message):
        try:
            print(f"Received wms_order_shipped (registering in CMS): {message}")
            service.new_order(message)
            print(f"Successfully registered order {message.get('order_id')} in CMS with package {message.get('package_id')}")
        except Exception as e:
            print(f"Failed to process wms_order_shipped in CMS for order {message.get('order_id')}: {e}")

    try:
        consume("cms_order_shipped", callback)
    except Exception as e:
        print(f"Failed to start cms_order_shipped consumer in CMS: {e}")

Thread(target=cms_new_order_listener, daemon=True).start()
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