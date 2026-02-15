from fastapi import FastAPI
import socket

wms = FastAPI()
s = None
    
@wms.get("/connect/{ip}/{port}")
def connect_to_server(ip: str, port: int):
    global s
    s = socket.socket()
    try:
        s.connect((ip, port))
    except Exception as e:
        s = None
        return {"response": f"Failed to connect to server at {ip}:{port}", "error": str(e)}
    return {"response": f"Connected to server at {ip}:{port}", "server_response": s.recv(1024).decode()}

@wms.get("/disconnect")
def disconnect_from_server():
    global s
    if s is None:
        return {"response": "Not connected to server"}
    s.send("exit\n".encode('ascii'))
    response = recvAll(s)
    s.close()
    s = None
    return {"response": f"Disconnected from server", "server_response": response}

@wms.get("/add")
def add_item():
    if s is None:
        return {"response": "Not connected to server"}
    s.send("add\n".encode('ascii'))
    response = recvAll(s)
    return ssvToDict(response)

@wms.get("/pack/{item_id}")
def pack_item(item_id: int):
    if s is None:
        return {"response": "Not connected to server"}
    s.send(f"pack {item_id}\n".encode('ascii'))
    response = recvAll(s)
    return ssvToDict(response)

@wms.get("/ship/{item_id}")
def ship_item(item_id: int):
    if s is None:
        return {"response": "Not connected to server"}
    s.send(f"ship {item_id}\n".encode('ascii'))
    response = recvAll(s)
    return ssvToDict(response)

@wms.get("/state/{item_id}")
def get_item_state(item_id: int):
    if s is None:
        return {"response": "Not connected to server"}
    s.send(f"state {item_id}\n".encode('ascii'))
    response = recvAll(s)
    return ssvToDict(response)

@wms.get("/list")
def list_items():
    if s is None:
        return {"response": "Not connected to server"}
    s.send("list\n".encode('ascii'))
    response = recvAll(s)
    return ssvToDict(response)

def ssvToDict(ssv_string):
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

def recvAll(sock):
    data = b""
    while True:
        part = sock.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data.decode()
    

# Legacy_Server_IP = "127.0.0.1"
# Legacy_Server_PORT = 5000

# s = socket.socket()
# s.connect((Legacy_Server_IP, Legacy_Server_PORT))

# print(s.recv(1024).decode())
