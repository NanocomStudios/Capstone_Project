
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
import asyncio
import httpx
from app.services.ros_adapter.ros_adapter import ROSConfig, ROSAdapter
from app.core.config import SERVICE_REGISTRY_URL, ROS_LEGACY_URL, ROS_ADAPTER_URL

async def register_with_registry():
    registry_url = SERVICE_REGISTRY_URL + "/register"
    my_info = {
        "name": "ros-service",
        "address": ROS_ADAPTER_URL
    }
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
               
                await client.post(registry_url, json=my_info, timeout=5)
            except Exception as e:
                print(f"Connection to Registry failed: {e}")
            
            await asyncio.sleep(20)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(register_with_registry())
    print("Service starting: Registering with service registry...")
    
    yield 
    
    task.cancel()
    print("Service shutting down: Cleaning up resources.")


config = ROSConfig(
    base_url=ROS_LEGACY_URL,
    timeout=3
)

ros_adapter = ROSAdapter(config)

app = FastAPI(title="ROS API Gateway", lifespan=lifespan)


class Stop(BaseModel):
    address: str
    packageId: str

class RouteRequest(BaseModel):
    vehicleId: str
    stops: List[Stop]


@app.post("/routes")
def create_route(request: RouteRequest):
    """
    Creates a new optimized route using ROSAdapter
    """
    try:
        result = ros_adapter.create_route(
            vehicle_id=request.vehicleId,
            stops=[stop.dict() for stop in request.stops]
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"ROS Service unavailable: {str(e)}"
        )


@app.get("/routes/{route_id}")
def get_route(route_id: str):
    """
    Fetch route details
    """
    try:
        result = ros_adapter.get_route(route_id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch route: {str(e)}"
        )


@app.get("/health")
def health_check():
    """
    Health endpoint for this API layer
    """
    return {"status": "ROS API Gateway Running"}
