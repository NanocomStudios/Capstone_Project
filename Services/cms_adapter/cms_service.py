import requests
import xmltodict

import os

class CMSService:

    def __init__(self, registry_url="http://localhost:8001"):
        self.registry_url = registry_url
        print(registry_url)

    def register_cms_adapter(self, address):
        req = {"name":"cms-adapter","address" : str(address)}
        r = requests.post("http://" + self.registry_url + "/register", json=req)
        if(r.status_code == 200):
            print("Registered on the service registery")
        else:
            print("Failed to register on the service registery")

    # def _discover_cms(self):
    #     r = requests.get(f"{self.registry_url}/discover/CMS")
    #     r.raise_for_status()
    #     return r.json()["address"]

    def _send_request(self, xml_body):
        base_url = os.getenv("LEGACY_CMS_HOST", "localhost") + ":8000"

        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            f"http://{base_url}/soap",
            data=xml_body,
            headers=headers
        )

        response.raise_for_status()
        ordered_dict = xmltodict.parse(response.text)
        return dict(ordered_dict["Response"])

    def login(self, username, password):
        xml_body = f"""
        <Request>
            <Action>login</Action>
            <Username>{username}</Username>
            <Password>{password}</Password>
        </Request>
        """
        return self._send_request(xml_body)

    def new_order(self, order):
        xml_body = f"""
        <Request>
            <Action>newOrder</Action>
            <OrderID>{order["order_id"]}</OrderID>
            <PackageID>{order["package_id"]}</PackageID>
            <ClientID>{order["client_id"]}</ClientID>
            <Address>{order["delivery_address"]}</Address>
            <CustomerName>{order["customer_name"]}</CustomerName>
        </Request>
        """
        return self._send_request(xml_body)

    def view_orders(self):
        xml_body = """
        <Request>
            <Action>viewOrders</Action>
        </Request>
        """
        return self._send_request(xml_body)

    def order_status(self, order_id):
        xml_body = f"""
        <Request>
            <Action>orderStatus</Action>
            <OrderID>{order_id}</OrderID>
        </Request>
        """
        return self._send_request(xml_body)

    def client_orders(self, client_id):
        xml_body = f"""
        <Request>
            <Action>clientOrders</Action>
            <ClientID>{client_id}</ClientID>
        </Request>
        """
        return self._send_request(xml_body)

    def view_bill(self, order_id):
        xml_body = f"""
        <Request>
            <Action>viewBill</Action>
            <OrderID>{order_id}</OrderID>
        </Request>
        """
        return self._send_request(xml_body)
