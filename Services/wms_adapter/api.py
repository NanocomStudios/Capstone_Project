import time
from fastapi import FastAPI
from adapter import WMSAdapter
from pubsub_adapter import WMSPubSubAdapter
from threading import Thread
import os
import requests
import socket

def register_on_service_reg():
    registry = socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_REG_PORT", 8001))
    service = socket.gethostbyname(os.getenv("SERVICE_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_PORT", 8002))

    req = {"name":"wms-adapter","address" : str(service)}
    r = requests.post("http://" + registry + "/register", json=req)
    if(r.status_code == 200):
        print("Registered on the service registery")
        return True
    else:
        print("Failed to register on the service registery")
        return False

if(register_on_service_reg() != True):
    exit(-1)

wms = FastAPI()
adapter = WMSAdapter()
print(os.getenv("LEGACY_WMS_HOST", "localhost"), os.getenv("LEGACY_WMS_PORT", 8000))

while(adapter.connect(os.getenv("LEGACY_WMS_HOST", "localhost"), int(os.getenv("LEGACY_WMS_PORT", 8000)))["status"] != "success"):
    print("Failed to connect to server, retrying...")
    time.sleep(30)

pubsub_adapter = WMSPubSubAdapter(os.getenv("LEGACY_WMS_HOST", "localhost"), int(os.getenv("LEGACY_WMS_PORT", 8000)))
listener_thread = Thread(target=pubsub_adapter.listen)
listener_thread.start()


@wms.get("/disconnect")
def disconnect_from_server():
    try:
        return adapter.disconnect()
    except Exception as e:
        return {"response": f"Error", "error": str(e)}
    

@wms.get("/add")
def add_item():
    try:
        return adapter.add_item()
    except Exception as e:
        return {"response": f"Error", "error": str(e)}

@wms.get("/pack/{item_id}")
def pack_item(item_id: int):
    try:
        return adapter.pack_item(item_id)
    except Exception as e:
        return {"response": f"Error", "error": str(e)}

@wms.get("/ship/{item_id}")
def ship_item(item_id: int):
    try:
        return adapter.ship_item(item_id)
    except Exception as e:
        return {"response": f"Error", "error": str(e)}

@wms.get("/state/{item_id}")
def get_item_state(item_id: int):
    try:
        return adapter.get_item_state(item_id)
    except Exception as e:
        return {"response": f"Error", "error": str(e)}

@wms.get("/list")
def list_items():
    try:
        return adapter.list_items()
    except Exception as e:
        return {"response": f"Error", "error": str(e)}
    
@wms.get("/health")
def health_check():
    return {"status": "UP"}


