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
    items: List[OrderItem]

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
    items: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    events: List[Dict[str, Any]]
    estimated_delivery: Optional[str] = None
    error: Optional[str] = None