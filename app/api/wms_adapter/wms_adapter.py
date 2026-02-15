from fastapi import FastAPI
from app.services.wms_adapter.wms_adapter import WMSAdapter

wms = FastAPI()
adapter = WMSAdapter()

@wms.get("/connect/{ip}/{port}")
def connect_to_server(ip: str, port: int):
    return adapter.connect(ip,port)

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


