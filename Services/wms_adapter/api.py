import time
from fastapi import FastAPI
from adapter import WMSAdapter
import os



wms = FastAPI()
adapter = WMSAdapter()

while(adapter.connect(os.getenv("LEGACY_WMS_HOST", "127.0.0.1"), int(os.getenv("LEGACY_WMS_PORT", 8000)))["status"] != "success"):
    print("Failed to connect to server, retrying...")
    time.sleep(30)

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


