import socket

class ServerBuilder:
    def __init__(
        self, 
        address: str = "127.0.0.1",
        port: int = 48751,
        *,
        timeout: int = 3
    ) -> None:
        self.address = address
        self.port = port
        self.timeout = timeout
    
    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(self.timeout)
        return self
    
    def run(self):
        while True:
            try:
                conn, addr = self.socket.accept()
            except socket.timeout:
                continue
            data = bytearray()
            while packet := conn.recv(8192):
                data.extend(packet)