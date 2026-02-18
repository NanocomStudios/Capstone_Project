from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

routes_db = {}

class Stop(BaseModel):
    address: str
    packageId: str

class RouteRequest(BaseModel):
    vehicleId: str
    stops: List[Stop]

@app.post("/routes")
def create_route(request: RouteRequest):
    route_id = str(uuid.uuid4())

    # Fake optimization logic
    optimized = list(reversed(request.stops))

    route_data = {
        "routeId": route_id,
        "vehicleId": request.vehicleId,
        "optimizedStops": optimized,
        "estimatedTime": f"{len(optimized)*20} minutes"
    }

    routes_db[route_id] = route_data
    return route_data

@app.get("/routes/{route_id}")
def get_route(route_id: str):
    return routes_db.get(route_id, {"error": "Route not found"})

@app.get("/health")
def health_check():
    return {"status": "UP"}
