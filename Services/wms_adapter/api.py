import time
from fastapi import FastAPI, HTTPException
from adapter import WMSAdapter
from pubsub_adapter import WMSPubSubAdapter
from Lib.publisher import consume, publish
from threading import Thread
import os
import requests
import socket

adapter = WMSAdapter()

def wms_failed_listener(message):
    print(f"Received failed message for order {message.get('order_id')}: {message.get('error')}")


def wms_add_listener():

    def callback(message):
        order_id       = message.get("order_id")
        delivery_address = message.get("delivery_address", "")
        client_id      = message.get("client_id", "")
        customer_name  = message.get("customer_name", "")

        try:
            # 1. Add item to legacy WMS
            add_response = adapter.add_item()
            print(f"WMS add response for order {order_id}: {add_response}")

            # Extract the real package_id assigned by the legacy WMS.
            # Response format: {"response": [{"added": "<id>"}, ...]}
            items = add_response.get("response", [])
            package_id = None
            for item in items:
                if "added" in item:
                    package_id = item["added"]
                    break

            if package_id is None:
                print(f"WMS add did not return a package id for order {order_id}. Cannot continue.")
                return

            # 2. Pack
            pack_response = adapter.pack_item(int(package_id))
            print(f"WMS pack response for order {order_id} / package {package_id}: {pack_response}")

            # 3. Ship
            ship_response = adapter.ship_item(int(package_id))
            print(f"WMS ship response for order {order_id} / package {package_id}: {ship_response}")

            # 4. Notify CMS + Delivery via a single event
            publish("wms_order_shipped", {
                "order_id":         order_id,
                "package_id":       package_id,
                "delivery_address": delivery_address,
                "client_id":        client_id,
                "customer_name":    customer_name,
            }, failed_function=wms_failed_listener, faild_func_route_key="wms_add_failed", ttl=5000)
            print(f"Published wms_order_shipped for order {order_id} / package {package_id}")

        except Exception as e:
            print(f"Error processing wms_add_request for order {order_id}: {e}")

    consume("wms_add_request", callback)

Thread(target=wms_add_listener).start()

def wms_pack_listener():

    def callback(message):
        package_id = message.get("package_id")
        try:
            pack_response = adapter.pack_item(int(package_id))
            print(f"WMS pack response for package {package_id}: {pack_response}")
        except Exception as e:
            print(f"Error processing wms_pack_request for package {package_id}: {e}")

    consume("wms_pack_request", callback)

Thread(target=wms_pack_listener).start()

def wms_ship_listener():

    def callback(message):
        package_id = message.get("package_id")
        try:
            ship_response = adapter.ship_item(int(package_id))
            print(f"WMS ship response for package {package_id}: {ship_response}")

            publish("wms_order_shipped", {
                "order_id":         order_id,
                "package_id":       package_id,
                "delivery_address": delivery_address,
                "client_id":        client_id,
                "customer_name":    customer_name,
            })
            print(f"Published wms_order_shipped for order {order_id} / package {package_id}")

        except Exception as e:
            print(f"Error processing wms_ship_request for package {package_id}: {e}")

    consume("wms_ship_request", callback)

Thread(target=wms_ship_listener).start()

def register_on_service_reg():
    registry = socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost")) + ":" + str(8000)
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
        raise HTTPException(status_code=500, detail=str(e))
    

@wms.get("/add")
def add_item():
    try:
        return adapter.add_item()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@wms.get("/pack/{item_id}")
def pack_item(item_id: int):
    try:
        return adapter.pack_item(item_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@wms.get("/ship/{item_id}")
def ship_item(item_id: int):
    try:
        return adapter.ship_item(item_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@wms.get("/state/{item_id}")
def get_item_state(item_id: int):
    try:
        return adapter.get_item_state(item_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@wms.get("/list")
def list_items():
    try:
        return adapter.list_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@wms.get("/health")
def health_check():
    return {"status": "UP"}


