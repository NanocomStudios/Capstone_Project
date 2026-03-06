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
from Lib.publisher import publish_to_failure_queue

# wms_add_listener removed - wms_adapter now owns the full add→pack→ship lifecycle
# and publishes wms_order_shipped when done.

def delivery_feedback_listener():
    def callback(message):
        try:
            order_id = message.get("order_id")
            delivery_id = message.get("delivery_id")
            status = message.get("status")
            reason = message.get("reason", "")
            print(f"Received delivery feedback for order {order_id} (delivery {delivery_id}): status {status}")

            if order_id in orders:
                order = orders[order_id]
                new_status = OrderStatus.COMPLETED if status == "delivered" else OrderStatus.FAILED
                
                order["status"] = new_status
                order["updated_at"] = datetime.now().isoformat()
                if "events" not in order:
                    order["events"] = []
                    
                event_desc = f"Delivery {status}"
                if reason:
                    event_desc += f" - Reason: {reason}"
                    
                order["events"].append({
                    "status": new_status,
                    "timestamp": datetime.now().isoformat(),
                    "description": event_desc
                })
                print(f"Updated local order {order_id} status to {new_status}")
            else:
                print(f"Order {order_id} not found locally to update feedback.")

        except Exception as e:
            print(f"Failed to process delivery feedback: {e}")
            publish_to_failure_queue("order_service.delivery_feedback.processing_failed", message, e)

    import time
    while True:
        try:
            consume("delivery_feedback", callback)
        except Exception as e:
            print(f"Failed to start delivery_feedback consumer: {e}")
            time.sleep(5)

Thread(target=delivery_feedback_listener, daemon=True).start()


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
        
        # Publish to WMS with full order context so wms_adapter can run add→pack→ship
        # and then notify CMS + Delivery via wms_order_shipped.
        publish("wms_add_request", {
            "order_id":         order_id,
            "delivery_address": order.delivery_address,
            "client_id":        order.client_id,
            "customer_name":    order.customer_name,
        })
        print(f"Published wms_add_request for order {order_id}")
        
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
        publish_to_failure_queue("order_service.order_creation.processing_failed", {"order_id": order_id, "order": order.dict()}, e)

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