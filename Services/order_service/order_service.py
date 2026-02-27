from fastapi import FastAPI, HTTPException, BackgroundTasks
from models import OrderRequest, OrderResponse, OrderStatus, OrderStatusDetail
from Lib.publisher import consume, publish
from registry_client import register_service
from uuid import uuid4
from datetime import datetime
from threading import Thread
import httpx
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware

wms_add_queue = []
def wms_add_listener():
    while True:
        def callback(message):
            order_id = message.get("order_id")
            if(order_id in wms_add_queue):
                wms_add_queue.remove(order_id)
                response = message.get("response")
                print(f"Received WMS add response for order {order_id}: {response}")
        consume("wms_add_response", callback)

Thread(target=wms_add_listener).start()


app = FastAPI(title="Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Store orders with more details
orders = {}

#Service URLs
CMS_ADAPTER_URL = os.getenv("CMS_ADAPTER_URL", "http://cms-adapter:8000")
ROS_ADAPTER_URL = os.getenv("ROS_ADAPTER_URL", "http://ros-adapter:8000")
WMS_ADAPTER_URL = os.getenv("WMS_ADAPTER_URL", "http://wms-adapter:8000")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
DELIVERY_SERVICE_URL = os.getenv("DELIVERY_SERVICE_URL", "http://delivery-service:8000")

# @app.on_event("startup")
# async def startup():
register_service("order-service", "http://order-service:8000")
print("Order Service started")

@app.post("/orders")
async def create_order(order: OrderRequest, background_tasks: BackgroundTasks):
    """Create a new order"""
    order_id = str(uuid4())
    
    #Process in background
    background_tasks.add_task(process_order, order_id, order)
    
    return OrderResponse(
        order_id=order_id,
        status=OrderStatus.RECEIVED,
        message="Order received"
    )

@app.get("/orders/{order_id}")
async def get_order_status(order_id: str):
    """VIEW ORDER STATUS - Get detailed order status"""
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = orders[order_id]
    
    #Return detailed status
    return OrderStatusDetail(
        order_id=order_id,
        status=order["status"],
        client_id=order["client_id"],
        delivery_address=order["delivery_address"],
        created_at=order["created_at"],
        updated_at=order["updated_at"],
        events=order.get("events", []),
        estimated_delivery=order.get("estimated_delivery"),
        error=order.get("error")
    )

@app.get("/orders/client/{client_id}")
async def get_client_orders(client_id: str):
    """Get all orders for a specific client"""
    client_orders = []
    for order_id, order in orders.items():
        if order["client_id"] == client_id:
            client_orders.append({
                "order_id": order_id,
                "status": order["status"],
                "created_at": order["created_at"],
                "delivery_address": order["delivery_address"]
            })
    
    return {
        "client_id": client_id,
        "total_orders": len(client_orders),
        "orders": client_orders
    }

@app.post("/pack")
async def pack_order(order_id: str):
    order_info = httpx.get(f"{CMS_ADAPTER_URL}/orders/{order_id}", timeout=5)
    if order_info.status_code != 200:
        return {"response": "Failed to retrieve order info from CMS"}
    order_data = order_info.json()
    print(order_data)
    package_id = order_data.get("Order").get("PackageID")

    wms_response = httpx.get(f"{WMS_ADAPTER_URL}/pack/{package_id}", timeout=5)
    if wms_response.status_code != 200:
        return {"response": "Failed to pack order in WMS"}
    
    return {"response": "Order packed successfully"}

@app.post("/ship")
async def ship_order(order_id: str):
    order_info = httpx.get(f"{CMS_ADAPTER_URL}/orders/{order_id}", timeout=5)
    if order_info.status_code != 200:
        return {"response": "Failed to retrieve order info from CMS"}
    order_data = order_info.json()
    package_id = order_data.get("Order").get("PackageID")
    delivery_address = order_data.get("Order").get("Address")

    wms_response = httpx.get(f"{WMS_ADAPTER_URL}/ship/{package_id}", timeout=5)
    if wms_response.status_code != 200:
        return {"response": "Failed to ship order in WMS"}
    
    driver_response = httpx.get(f"{AUTH_SERVICE_URL}/select_driver", timeout=5)
    if driver_response.status_code != 200:
        return {"response": "Failed to select driver"}
    
    driver_data = driver_response.json()
    driver_id = driver_data.get("driver")

    delivery_response = httpx.post(f"{DELIVERY_SERVICE_URL}/deliveries/assign", json={
        "order_id": order_id,
        "driver_id": driver_id,
        "package_id": package_id,
        "delivery_address": delivery_address
    }, timeout=5)

    if delivery_response.status_code != 200:
        return {"response": "Failed to assign driver to delivery"}

    return {"response": "Order shipped successfully"}


def process_order(order_id: str, order: OrderRequest):
    """Process order through all systems"""
    try:
        # #Update status
        # await update_order_status(order_id, OrderStatus.PROCESSING, "Processing order")
        
        # #Send to CMS
        # async with httpx.AsyncClient() as client:
        #     cms_response = await client.post(
        #         f"{CMS_ADAPTER_URL}/login",
        #         json={"username": order.client_id, "password": "1234"},
        #         timeout=5
        #     )
            
        #     if cms_response.status_code != 200:
        #         raise Exception("CMS failed")
        
        # await update_order_status(order_id, OrderStatus.PROCESSING, "CMS updated")
        
        #Send to WMS
        # async with httpx.AsyncClient() as client:
            # for item in order.items:
            #     for i in range(item.quantity):
        wms_add_queue.append(order_id)
        publish("wms_add_request", {"order_id": order_id});

        # wms_response = httpx.get(f"{WMS_ADAPTER_URL}/add", timeout=5)
        # if wms_response.status_code != 200:
        #     raise Exception("WMS failed")
        
        # package_id = wms_response.json().get("response")[0]["added"]
        
        
        cms_resopnse = httpx.post(f"{CMS_ADAPTER_URL}/new_order", json={
            "order_id": order_id,
            "package_id": package_id,
            "client_id": order.client_id,
            "delivery_address": order.delivery_address,
            "customer_name": order.customer_name
        }, timeout=5)

        if cms_resopnse.status_code != 200:
            raise Exception("CMS failed to register order")
        # print("Package ID :- " + str(package_id))

        # await update_order_status(order_id, OrderStatus.PROCESSING, "Items added to warehouse")
        
        # #Send to ROS
        # async with httpx.AsyncClient() as client:
        #     ros_response = await client.post(
        #         f"{ROS_ADAPTER_URL}/routes",
        #         json={
        #             "vehicleId": "vehicle1",
        #             "stops": [{
        #                 "address": order.delivery_address,
        #                 "packageId": order_id
        #             }]
        #         },
        #         timeout=5
        #     )
            
        #     if ros_response.status_code != 200:
        #         raise Exception("ROS failed")
            
        #     #Get estimated delivery time from ROS if available
        #     ros_data = ros_response.json()
        #     if "estimatedTime" in ros_data:
        #         orders[order_id]["estimated_delivery"] = ros_data["estimatedTime"]
        
        # await update_order_status(order_id, OrderStatus.COMPLETED, "Order completed successfully")
        
        #Publish event
        publish("order_events", {
            "order_id": order_id,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        # orders[order_id]["status"] = OrderStatus.FAILED
        # orders[order_id]["error"] = str(e)
        # orders[order_id]["updated_at"] = datetime.now().isoformat()
        
        # #Add failure event
        # if "events" in orders[order_id]:
        #     orders[order_id]["events"].append({
        #         "status": OrderStatus.FAILED,
        #         "timestamp": datetime.now().isoformat(),
        #         "description": f"Failed: {str(e)}"
        #     })
        
        print(f"Order {order_id} failed: {e}")

# def wms_add_request_listener():


async def update_order_status(order_id: str, status: OrderStatus, description: str):
    """Helper to update order status and add event"""
    if order_id in orders:
        orders[order_id]["status"] = status
        orders[order_id]["updated_at"] = datetime.now().isoformat()
        
        if "events" not in orders[order_id]:
            orders[order_id]["events"] = []
        
        orders[order_id]["events"].append({
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "description": description
        })

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "order_service",
        "total_orders": len(orders)
    }