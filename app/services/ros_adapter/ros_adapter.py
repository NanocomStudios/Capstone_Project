import requests
from requests.exceptions import RequestException

class ROSConfig:
    def __init__(self, base_url="http://localhost:8001", timeout=3):
        self.base_url = base_url
        self.timeout = timeout
        
class ROSAdapter:

    def __init__(self, config: ROSConfig):
        self.base_url = config.base_url
        self.timeout = config.timeout

    def _check_health(self):
        try:
            r = requests.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            return r.status_code == 200
        except RequestException:
            return False

    def create_route(self, vehicle_id, stops):
        if not self._check_health():
            raise Exception("ROS service is offline")

        payload = {
            "vehicleId": vehicle_id,
            "stops": stops
        }

        try:
            response = requests.post(
                f"{self.base_url}/routes",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            raise Exception(f"Failed to create route: {e}")

    def get_route(self, route_id):
        try:
            response = requests.get(
                f"{self.base_url}/routes/{route_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to fetch route: {e}")
