from fastapi import FastAPI
from pydantic import BaseModel
from cms_service import CMSService

app = FastAPI(title="CMS Adapter")

service = CMSService()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    return service.login(req.username, req.password)

@app.get("/orders")
def view_orders():
    return service.view_orders()

@app.get("/orders/{order_id}")
def order_status(order_id: str):
    return service.order_status(order_id)

@app.get("/bill/{order_id}")
def view_bill(order_id: str):
    return service.view_bill(order_id)