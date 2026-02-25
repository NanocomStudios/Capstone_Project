from fastapi import FastAPI
import requests
import socket
import os

def register_on_service_reg():
    registry = socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_REG_PORT", 8001))
    service = socket.gethostbyname(os.getenv("SERVICE_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_PORT", 8002))

    req = {"name":"api-gateway","address" : str(service)}
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

@app.post("/")
