import httpx
import asyncio

REGISTRY_URL = "http://service-registry:8000"

async def register_service(name: str, address: str):
    """Register with service registry"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{REGISTRY_URL}/register",
                json={"name": name, "address": address},
                timeout=5
            )
            if response.status_code == 200:
                print(f"Registered {name}")
            else:
                print(f"Registration failed: {response.status_code}")
    except Exception as e:
        print(f"Registry unavailable: {e}")