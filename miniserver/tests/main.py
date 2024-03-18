import socket
import json
import struct

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
    
    def _get_data_size(self) -> int:
        header = self.client_socket.recv(4)
        if not header:
            raise Exception("TODO")
        return struct.unpack('!I', header)[0]
    
    def send_message(self, message):
        header = struct.pack('!I', len(message))
        self.client_socket.sendall(header)
        self.client_socket.sendall(message)
        return self
    
    def recv(self) -> bytearray:
        data = bytearray()
        remaining_size = self._get_data_size()
        while remaining_size > 0:
            chunk = self.client_socket.recv(min(8192, remaining_size))
            if not chunk:
                break
            data.extend(chunk)
            remaining_size -= len(chunk)
        return data
    
    def close(self):
        self.client_socket.close()
            

def main():
    message = {
        "username": "loled",
        "old_password": "123",
        "new_password": "123"
    }
    message_str = json.dumps(message)
    message_byte = message_str.encode()
    tester = TestBuilder()
    data = tester.connect().send_message(message_byte).recv()
    print(data.decode())
    tester.close()
    
    
if __name__ == "__main__":
    main()