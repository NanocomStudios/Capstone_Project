import socket
from time import time
import asyncio
import pika
import os

from adapter import WMSAdapter

class WMSPubSubAdapter:
    def __init__(self, host: str, port: int):
        self.host = host
        self.wmsAdapter = WMSAdapter()

        while(self.wmsAdapter.connect(host, port)["status"] != "success"):
            print("Failed to connect the listner, retrying...")
            time.sleep(30)
    
        self.s = self.wmsAdapter.s
    
    def listen(self):
        if self.s is None:
            return {"response": "Not connected to server"}
        

        self.s.send("listen\n".encode('ascii'))
        response = self.recvAll(self.s)
        print("Started listening for updates from server:", response)

        while True:
            response = self.recvAll(self.s)
            message = self.ssvToDict(response)
            print("Received update from server:", message)
            
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))
            channel = connection.channel()
            channel.exchange_declare(exchange='wms', exchange_type='fanout')
            channel.basic_publish(exchange='wms', routing_key='', body=str(message))
            connection.close()

    def recvAll(self, sock):
        data = b""
        while True:
            part = sock.recv(1024)
            data += part
            if len(part) < 1024:
                break
        return data.decode()
    
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