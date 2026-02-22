import httpx
from typing import List, Dict, Any

class ROSClient:
    """
    HTTP client wrapper for the Legacy Route Optimisation System (ROS).

    The ROS exposes:
        POST /routes    { vehicleId, stops: [{address, packageId}] }
        GET  /routes/{route_id}
        GET  /health
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def calculate_route(self, vehicle_id: str, stops: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        calculateRoute() — Submit a route-optimisation request to ROS.
        Returns JSON with routeId, optimisedStops, estimatedTime from the ROS.
        """
        payload = {"vehicleId": vehicle_id, "stops": stops}
        with httpx.Client(timeout=10.0) as client:
            response = client.post(f"{self.base_url}/routes", json=payload)
            response.raise_for_status()
            return response.json()

    def get_route(self, route_id: str) -> Dict[str, Any]:
        """Retrieve an existing route by its ID from ROS."""
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{self.base_url}/routes/{route_id}")
            response.raise_for_status()
            return response.json()
