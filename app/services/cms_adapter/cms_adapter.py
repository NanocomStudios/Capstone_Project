import requests

def get_cms_address():
    r = requests.get("http://localhost:8500/discover/CMS")
    return r.json()["address"]

class CMSAdapter:

    def __init__(self, registry_url="http://localhost:8500"):
        self.registry_url = registry_url

    def _get_base_url(self):
        response = requests.get(f"{self.registry_url}/discover/CMS")
        return response.json()["address"]

    def login(self, username, password):
        base_url = self._get_base_url()

        xml_body = f"""
        <Request>
            <Action>login</Action>
            <Username>{username}</Username>
            <Password>{password}</Password>
        </Request>
        """

        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            f"{base_url}/soap",
            data=xml_body,
            headers=headers
        )

        return response.text
