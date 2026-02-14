from fastapi import FastAPI, Request
from fastapi.responses import Response
import xml.etree.ElementTree as ET

app = FastAPI(title="Legacy CMS Service")

@app.post("/soap")
async def handle_request(request: Request):
    body = await request.body()
    root = ET.fromstring(body)

    action = root.find("Action").text

    if action == "login":
        username = root.find("Username").text

        response_xml = f"""
        <Response>
            <Status>Success</Status>
            <User>{username}</User>
        </Response>
        """

    elif action == "viewOrders":
        response_xml = """
        <Response>
            <Orders>
                <Order>ORD001</Order>
                <Order>ORD002</Order>
            </Orders>
        </Response>
        """

    elif action == "orderStatus":
        order_id = root.find("OrderId").text

        response_xml = f"""
        <Response>
            <OrderId>{order_id}</OrderId>
            <Status>Shipped</Status>
        </Response>
        """

    elif action == "viewBill":
        order_id = root.find("OrderId").text

        response_xml = f"""
        <Response>
            <OrderId>{order_id}</OrderId>
            <Amount>150.00</Amount>
        </Response>
        """

    else:
        response_xml = "<Response><Status>Unknown Action</Status></Response>"

    return Response(content=response_xml, media_type="application/xml")
