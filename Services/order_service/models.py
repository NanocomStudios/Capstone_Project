from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderRequest(BaseModel):
    client_id: str
    delivery_address: str

class OrderResponse(BaseModel):
    order_id: str
    status: OrderStatus
    message: Optional[str] = None

class OrderStatusDetail(BaseModel):
    """Detailed order status response"""
    order_id: str
    status: OrderStatus
    client_id: str
    delivery_address: str
    customer_name: str