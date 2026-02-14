from fastapi import APIRouter, Request
from fastapi.responses import Response
from .cms_data import users, orders
import xml.etree.ElementTree as ET

router = APIRouter()

@router.post("/soap")
async def soap_endpoint(request: Request):
    body = await request.body()
    root = ET.fromstring(body)

    action = root.find("Action").text

    if action == "login":
        username = root.find("Username").text
        password = root.find("Password").text
        
        if username in users and users[username]["password"] == password:
            return Response("<Response>SUCCESS</Response>", media_type="application/xml")
        else:
            return Response("<Response>FAILED</Response>", media_type="application/xml")

    elif action == "viewOrders":
        client = root.find("Client").text
        client_orders = [o for o in orders if orders[o]["client"] == client]

        response_xml = "<Orders>" + "".join([f"<Order>{o}</Order>" for o in client_orders]) + "</Orders>"
        return Response(response_xml, media_type="application/xml")

    elif action == "orderStatus":
        order_id = root.find("OrderId").text
        status = orders.get(order_id, {}).get("status", "NOT_FOUND")

        return Response(f"<Status>{status}</Status>", media_type="application/xml")
