"""
  GET  /deliveries/{delivery_id}/track       → TrackDelivery()
  GET  /drivers/{driver_id}/assignments      → viewOrderAssigned()
  POST /drivers/{driver_id}/routes           → ViewRoutes()  (calls Legacy ROS)
  POST /deliveries/{delivery_id}/feedback    → orderFeedback()

Helper endpoints:
  POST /deliveries/assign   — assign an order to a driver (called by Order Service)
  GET  /health              — liveness probe
"""

import os
import uuid
import requests
import socket
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import Base, Delivery, DeliveryFeedback, SessionLocal, engine
from ros_client import ROSClient

ROS_SERVICE_URL = os.getenv("ROS_SERVICE_URL", "http://localhost:8001")

ros = ROSClient(ROS_SERVICE_URL)

def register_on_service_reg():
    registry = socket.gethostbyname(os.getenv("SERVICE_REG_HOST", "localhost")) + ":" + str(8000)
    service = socket.gethostbyname(os.getenv("SERVICE_HOST", "localhost")) + ":" + str(os.getenv("SERVICE_PORT", 8005))

    req = {"name":"delivery-service","address" : str(service)}
    r = requests.post("http://" + registry + "/register", json=req)
    if(r.status_code == 200):
        print("Registered on the service registery")
        return True
    else:
        print("Failed to register on the service registery")
        return False

if(register_on_service_reg() != True):
    exit(-1)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="SwiftLogistics Delivery Service", lifespan=lifespan)

class Stop(BaseModel):
    address: str
    packageId: str


class RouteRequest(BaseModel):
    vehicleId: str
    stops: List[Stop]

class AssignDeliveryRequest(BaseModel):
    order_id: str
    driver_id: str
    package_id: str
    delivery_address: str

class FeedbackRequest(BaseModel):
    """
    Submitted by the driver when they complete (or fail) a delivery.

    - status:         'delivered' or 'failed'
    - reason:         Required when status is 'failed' (e.g. 'recipient not available')
    - signature_data: Base-64 encoded digital signature from the customer
    - photo_url:      URL / path of proof-of-delivery photo
    """
    status: str
    reason: Optional[str] = None
    signature_data: Optional[str] = None
    photo_url: Optional[str] = None


@app.get("/health")
def health_check():
    return {"status": "UP", "service": "delivery-service"}


@app.post("/deliveries/assign", status_code=201)
def assign_delivery(req: AssignDeliveryRequest):
    """
    Assign an order/package to a driver.
    Called by the Order Service (directly or via the service registry).
    """
    db = SessionLocal()
    try:
        delivery = Delivery(
            id=str(uuid.uuid4()),
            order_id=req.order_id,
            driver_id=req.driver_id,
            package_id=req.package_id,
            delivery_address=req.delivery_address,
            status="assigned",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return {"message": "Delivery assigned", "delivery_id": delivery.id}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        db.close()


@app.get("/deliveries/{delivery_id}/track")
def track_delivery(delivery_id: str):
    """
    TrackDelivery() — Return real-time status of a delivery.
    Used by Client Portal to show order-tracking to e-commerce clients.
    """
    db = SessionLocal()
    try:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        return {
            "delivery_id": delivery.id,
            "order_id": delivery.order_id,
            "package_id": delivery.package_id,
            "driver_id": delivery.driver_id,
            "status": delivery.status,
            "delivery_address": delivery.delivery_address,
            "last_updated": delivery.updated_at,
        }
    finally:
        db.close()


@app.get("/drivers/{driver_id}/assignments")
def view_order_assigned(driver_id: str):
    """
    viewOrderAssigned() — Return the full delivery manifest for a driver.
    The driver mobile app calls this to list all pending/in-transit packages.
    """
    db = SessionLocal()
    try:
        deliveries = (
            db.query(Delivery)
            .filter(
                Delivery.driver_id == driver_id,
                Delivery.status.in_(["assigned", "in_transit"]),
            )
            .order_by(Delivery.created_at)
            .all()
        )
        return {
            "driver_id": driver_id,
            "total": len(deliveries),
            "assignments": [
                {
                    "delivery_id": d.id,
                    "order_id": d.order_id,
                    "package_id": d.package_id,
                    "delivery_address": d.delivery_address,
                    "status": d.status,
                    "created_at": d.created_at,
                }
                for d in deliveries
            ],
        }
    finally:
        db.close()


@app.post("/drivers/{driver_id}/routes")
def view_routes(driver_id: str, req: RouteRequest):
    """
    ViewRoutes() — Fetch an optimised route from the Legacy ROS.
    The driver mobile app calls this to get the most efficient delivery order for the day.
    Delegates to Legacy ROS via HTTP (httpx).
    """
    try:
        route = ros.calculate_route(
            vehicle_id=req.vehicleId,
            stops=[stop.model_dump() for stop in req.stops],
        )
        return route
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to reach ROS service: {exc}",
        )


@app.post("/deliveries/{delivery_id}/feedback", status_code=201)
def order_feedback(delivery_id: str, req: FeedbackRequest):
    """
    orderFeedback() — Driver submits delivery outcome.

    Accepts:
      - status:         'delivered' or 'failed'
      - reason:         failure reason (required if failed)
      - signature_data: base-64 customer signature
      - photo_url:      proof-of-delivery photo URL

    Updates delivery status in PostgreSQL.
    """
    if req.status not in ("delivered", "failed"):
        raise HTTPException(
            status_code=400,
            detail="status must be 'delivered' or 'failed'",
        )
    if req.status == "failed" and not req.reason:
        raise HTTPException(
            status_code=400,
            detail="reason is required when status is 'failed'",
        )

    db = SessionLocal()
    try:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")

        # Update delivery status
        delivery.status = req.status
        delivery.updated_at = datetime.utcnow()

        # Persist proof-of-delivery record
        feedback = DeliveryFeedback(
            id=str(uuid.uuid4()),
            delivery_id=delivery_id,
            status=req.status,
            reason=req.reason,
            signature_data=req.signature_data,
            photo_url=req.photo_url,
            timestamp=datetime.utcnow(),
        )
        db.add(feedback)
        db.commit()

        return {
            "message": f"Delivery marked as '{req.status}'",
            "delivery_id": delivery_id,
            "feedback_id": feedback.id,
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        db.close()
