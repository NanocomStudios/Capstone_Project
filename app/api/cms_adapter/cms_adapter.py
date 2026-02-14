from fastapi import FastAPI
from pydantic import BaseModel
from app.services.cms_service.cms_service import CMSService

app = FastAPI(title="CMS Adapter API")

cms_service = CMSService()

class LoginRequest(BaseModel):
    username: str
    password: str

class OrderRequest(BaseModel):
    order_id: str

@app.post("/login")
def login(req: LoginRequest):
    result = cms_service.login(req.username, req.password)
    return {"legacy_response": result}

@app.get("/orders")
def view_orders():
    result = cms_service.view_orders()
    return {"legacy_response": result}

@app.post("/order-status")
def order_status(req: OrderRequest):
    result = cms_service.order_status(req.order_id)
    return {"legacy_response": result}

@app.post("/bill")
def view_bill(req: OrderRequest):
    result = cms_service.view_bill(req.order_id)
    return {"legacy_response": result}
