from abc import ABC, abstractmethod
import socket
import json
from typing import Optional

class ConsumerAbstract(ABC):
    
    @abstractmethod
    def consume(self, data: bytearray) -> Optional[bytearray|bytes]:
        ...
    
    @abstractmethod
    def stop_loop(self) -> bool:
        ...
    
    @abstractmethod
    def handle_error(self, error: Exception) -> Optional[bytearray|bytes]:
        error_obj = {
            "error_code": 500,
            "message": "Server Error"
        }
        error_bytes = json.dumps(error_obj).encode()
        return error_bytes

class ServerBuilder:
    def __init__(
        self, 
        address: str = "127.0.0.1",
        port: int = 48751,
        *,
        timeout: int = 1
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

    def set_consumer(self, consumer: ConsumerAbstract):
        self.consumer = consumer
        return self

    def _get_data(self, conn: socket.socket) -> bytearray:
        data = bytearray()
        while packet := conn.recv(8192):
            data.extend(packet)
        return data
    
    def _error(
        self, 
        conn: Optional[socket.socket], 
        error_data: Optional[bytearray|bytes]
    ):
        if not error_data:
            return
        if not conn:
            return
        conn.sendall(error_data)
    
    def _loop(self):
        try:
            conn, _ = self.socket.accept()
            data = self._get_data(conn)
            return_data = self.consumer.consume(data)
            if return_data:
                conn.sendall(return_data)
        except socket.timeout:
            return
        except Exception as err:
            # TODO print error
            error_data = self.consumer.handle_error(err)
            return self._error(conn, error_data)
        finally:
            if conn:
                conn.close()

    def run(self):
        while not self.consumer.stop_loop() :
            self._loop()
            