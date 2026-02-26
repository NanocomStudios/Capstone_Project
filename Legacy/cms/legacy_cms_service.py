from fastapi import FastAPI, Request
from fastapi.responses import Response
import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, role TEXT)")
c.execute("INSERT OR IGNORE INTO users (username, role) VALUES ('bhanuka', 'client')")
c.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY, package_id TEXT, client_id TEXT, delivery_address TEXT, customer_name TEXT, FOREIGN KEY(client_id) REFERENCES users(username))")
conn.commit()
conn.close()

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

    elif action == "newOrder":
        order_id = root.find("OrderID").text
        package_id = root.find("PackageID").text
        client_id = root.find("ClientID").text
        address = root.find("Address").text
        customer_name = root.find("CustomerName").text

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)", (order_id, package_id, client_id, address, customer_name))
        conn.commit()
        conn.close()
        response_xml = f"""
        <Response>
            <Status>Order Received</Status>
        </Response>
        """

    elif action == "viewOrders":
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT order_id, package_id, client_id, delivery_address, customer_name FROM orders")
        orders = c.fetchall()

        orders_xml = ""
        for order in orders:
            orders_xml += f"""
            <Order>
                <OrderID>{order[0]}</OrderID>
                <PackageID>{order[1]}</PackageID>
                <ClientID>{order[2]}</ClientID>
                <Address>{order[3]}</Address>
                <CustomerName>{order[4]}</CustomerName>
            </Order>
            """
        response_xml = f"""
        <Response>
            {orders_xml}
        </Response>
        """
        conn.close()


    elif action == "orderStatus":
        order_id = root.find("OrderID").text

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT order_id, package_id, client_id, delivery_address, customer_name FROM orders WHERE order_id = ?", (order_id,))
        orders = c.fetchall()

        orders_xml = ""
        for order in orders:
            orders_xml += f"""
            <Order>
                <OrderID>{order[0]}</OrderID>
                <PackageID>{order[1]}</PackageID>
                <ClientID>{order[2]}</ClientID>
                <Address>{order[3]}</Address>
                <CustomerName>{order[4]}</CustomerName>
            </Order>
            """
        response_xml = f"""
        <Response>
            {orders_xml}
        </Response>
        """
        conn.close()

    elif action == "viewBill":
        order_id = root.find("OrderID").text

        response_xml = f"""
        <Response>
            <OrderID>{order_id}</OrderID>
            <Amount>150.00</Amount>
        </Response>
        """

    else:
        response_xml = "<Response><Status>Unknown Action</Status></Response>"

    return Response(content=response_xml, media_type="application/xml")
