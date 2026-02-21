import socket

class WMSAdapter:
    def __init__(self):
        self.s = None

    def connect(self, host: str, port: int):
        self.s = socket.socket()
        try:
            host_ip = socket.gethostbyname(host)
            print("Connecting to server at", host_ip, ":", port)
            self.s.connect((host_ip, port))
        except Exception as e:
            self.s = None
            return {"status": "failed", "response": f"Failed to connect to server at {host_ip}:{port}", "error": str(e)}
        return {"status": "success", "response": f"Connected to server at {host_ip}:{port}", "server_response": self.s.recv(1024).decode()}

    def disconnect(self):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send("exit\n".encode('ascii'))
        response = self.recvAll(self.s)
        self.s.close()
        self.s = None
        return {"response": f"Disconnected from server", "server_response": response}

    def add_item(self):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send("add\n".encode('ascii'))
        response = self.recvAll(self.s)
        return self.ssvToDict(response)

    def pack_item(self, item_id: int):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send(f"pack {item_id}\n".encode('ascii'))
        response = self.recvAll(self.s)
        return self.ssvToDict(response)

    def ship_item(self, item_id: int):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send(f"ship {item_id}\n".encode('ascii'))
        response = self.recvAll(self.s)
        return self.ssvToDict(response)

    def get_item_state(self, item_id: int):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send(f"state {item_id}\n".encode('ascii'))
        response = self.recvAll(self.s)
        return self.ssvToDict(response)
    
    def list_items(self):
        if self.s is None:
            return {"response": "Not connected to server"}
        self.s.send("list\n".encode('ascii'))
        response = self.recvAll(self.s)
        return self.ssvToDict(response)
    
    def ssvToDict(self, ssv_string):
        lines = ssv_string.split("\r\n")
        out = {"response": []}

        for line in lines:
            if len(line.strip()) == 0:
                continue

            words = line.split(' ')
            if len(words) == 0:
                continue
            elif len(words) == 1:
                out["response"].append({words[0]: ""})
            else:
                out["response"].append({words[0]: words[1]})
        return out

    def recvAll(self, sock):
        data = b""
        while True:
            part = sock.recv(1024)
            data += part
            if len(part) < 1024:
                break
        return data.decode()