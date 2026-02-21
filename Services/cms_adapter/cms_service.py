import requests

class CMSService:

    def __init__(self, registry_url="http://localhost:8500"):
        self.registry_url = registry_url

    def _discover_cms(self):
        r = requests.get(f"{self.registry_url}/discover/CMS")
        r.raise_for_status()
        return r.json()["address"]

    def _send_request(self, xml_body):
        base_url = self._discover_cms()

        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            f"{base_url}/soap",
            data=xml_body,
            headers=headers
        )

        response.raise_for_status()
        return response.text

    def login(self, username, password):
        xml_body = f"""
        <Request>
            <Action>login</Action>
            <Username>{username}</Username>
            <Password>{password}</Password>
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
            <OrderId>{order_id}</OrderId>
        </Request>
        """
        return self._send_request(xml_body)

    def view_bill(self, order_id):
        xml_body = f"""
        <Request>
            <Action>viewBill</Action>
            <OrderId>{order_id}</OrderId>
        </Request>
        """
        return self._send_request(xml_body)
