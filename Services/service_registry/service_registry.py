from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import time

app = FastAPI(title="SwiftLogistics Service Registry")

registry: Dict[str, dict] = {}

class ServiceSchema(BaseModel):
    name: str
    address: str  #like "http://192.168.1.50:8000"

@app.post("/register")
def register_service(service: ServiceSchema):
    registry[service.name] = {
        "address": service.address,
        "last_heartbeat": time.time()
    }
    print(f"Registered {service.name} at {service.address}")
    return {"status": "registered"}

@app.get("/discover/{service_name}")
def discover_service(service_name: str):
    if service_name not in registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    ## if the last heartbeat was more than 30 seconds ago, consider the service dead
    # if time.time() - registry[service_name]["last_heartbeat"] > 30:
    #     del registry[service_name]
    #     raise HTTPException(status_code=404, detail="Service timed out")
        
    return {"address": registry[service_name]["address"]}

@app.get("/list")
def list_services():
    return {"services": list(registry.keys())}

@app.get("/health")
def health():
    return {"services_online": list(registry.keys())}