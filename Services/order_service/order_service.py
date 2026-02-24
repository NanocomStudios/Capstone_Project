from fastapi import FastAPI, HTTPException, BackgroundTasks
from models import OrderRequest, OrderResponse, OrderStatus, OrderStatusDetail
from publisher import publish
from registry_client import register_service
from uuid import uuid4
from datetime import datetime
import httpx
import asyncio
import os

app = FastAPI(title="Order Service")

#Store orders with more details
orders = {}

#Service URLs
CMS_ADAPTER_URL = os.getenv("CMS_ADAPTER_URL", "http://cms-adapter:8000")
ROS_ADAPTER_URL = os.getenv("ROS_ADAPTER_URL", "http://ros-adapter:8000")
WMS_ADAPTER_URL = os.getenv("WMS_ADAPTER_URL", "http://wms-adapter:8000")

@app.on_event("startup")
async def startup():
    await register_service("order-service", "http://order-service:8000")
    print("Order Service started")

@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderRequest, background_tasks: BackgroundTasks):
    """Create a new order"""
    order_id = str(uuid4())
    
    #Store order with more details for status tracking
    orders[order_id] = {
        "order_id": order_id,
        "status": OrderStatus.RECEIVED,
        "client_id": order.client_id,
        "delivery_address": order.delivery_address,
        "items": [item.dict() for item in order.items],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "events": [
            {
                "status": OrderStatus.RECEIVED,
                "timestamp": datetime.now().isoformat(),
                "description": "Order received"
            }
        ]
    }
    
    #Process in background
    background_tasks.add_task(process_order, order_id, order)
    
    return OrderResponse(
        order_id=order_id,
        status=OrderStatus.RECEIVED,
        message="Order received"
    )

@app.get("/orders/{order_id}", response_model=OrderStatusDetail)
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
        items=order["items"],
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

async def process_order(order_id: str, order: OrderRequest):
    """Process order through all systems"""
    try:
        #Update status
        await update_order_status(order_id, OrderStatus.PROCESSING, "Processing order")
        
        #Send to CMS
        async with httpx.AsyncClient() as client:
            cms_response = await client.post(
                f"{CMS_ADAPTER_URL}/login",
                json={"username": order.client_id, "password": "1234"},
                timeout=5
            )
            
            if cms_response.status_code != 200:
                raise Exception("CMS failed")
        
        await update_order_status(order_id, OrderStatus.PROCESSING, "CMS updated")
        
        #Send to WMS
        async with httpx.AsyncClient() as client:
            for item in order.items:
                for i in range(item.quantity):
                    wms_response = await client.get(f"{WMS_ADAPTER_URL}/add", timeout=5)
                    if wms_response.status_code != 200:
                        raise Exception("WMS failed")
        
        await update_order_status(order_id, OrderStatus.PROCESSING, "Items added to warehouse")
        
        #Send to ROS
        async with httpx.AsyncClient() as client:
            ros_response = await client.post(
                f"{ROS_ADAPTER_URL}/routes",
                json={
                    "vehicleId": "vehicle1",
                    "stops": [{
                        "address": order.delivery_address,
                        "packageId": order_id
                    }]
                },
                timeout=5
            )
            
            if ros_response.status_code != 200:
                raise Exception("ROS failed")
            
            #Get estimated delivery time from ROS if available
            ros_data = ros_response.json()
            if "estimatedTime" in ros_data:
                orders[order_id]["estimated_delivery"] = ros_data["estimatedTime"]
        
        await update_order_status(order_id, OrderStatus.COMPLETED, "Order completed successfully")
        
        #Publish event
        publish("order_events", {
            "order_id": order_id,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        orders[order_id]["status"] = OrderStatus.FAILED
        orders[order_id]["error"] = str(e)
        orders[order_id]["updated_at"] = datetime.now().isoformat()
        
        #Add failure event
        if "events" in orders[order_id]:
            orders[order_id]["events"].append({
                "status": OrderStatus.FAILED,
                "timestamp": datetime.now().isoformat(),
                "description": f"Failed: {str(e)}"
            })
        
        print(f"Order {order_id} failed: {e}")

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