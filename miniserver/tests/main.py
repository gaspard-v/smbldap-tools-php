import socket
import json

class TestBuilder:
    def __init__(
        self, 
        address: str = "127.0.0.1", 
        port: int = 48751
    ) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
    
    def connect(self):
        self.client_socket.connect((self.address, self.port))
        return self
    
    def send_message(self, message):
        self.client_socket.sendall(message)
        return self
    
    def recv(self) -> bytearray:
        data = bytearray()
        while chunk := self.client_socket.recv(8192):
            data.extend(chunk)
        return data
            

def main():
    message = {
        "username": "loled",
        "old_password": "123",
        "new_password": "123"
    }
    message_str = json.dumps(message)
    message_byte = message_str.encode()
    tester = TestBuilder()
    recv = tester.connect().send_message(message_byte)
    
    
if __name__ == "__main__":
    main()