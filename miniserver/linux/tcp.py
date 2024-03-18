from abc import ABC, abstractmethod
from os import error
import socket
import json
import struct
from typing import Optional
from ..models.tcp.error import build_error_response
from dataclasses import asdict

class ConsumerAbstract(ABC):
    
    @abstractmethod
    def consume(self, data: bytearray) -> Optional[bytearray|bytes]:
        ...
    
    @abstractmethod
    def stop_loop(self) -> bool:
        ...
        
    def _get_error_message(self, error: Exception, status_code: int) -> bytes:
        error_obj = build_error_response(
            status_code,
            str(type(error)),
            str(error)
        )
        error_dict = asdict(error_obj)
        return json.dumps(error_dict).encode()
    
    @abstractmethod
    def handle_error(self, error: Exception) -> Optional[bytearray|bytes]:
        return self._get_error_message(error, 500)

class ServerBuilder:
    def __init__(
        self, 
        address: str = "127.0.0.1",
        port: int = 48751,
        *,
        timeout: int = 1,
        buffer_size: int = 8192,
        header_size: int = 4
    ) -> None:
        self.address = address
        self.port = port
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.header_size = header_size
    
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
    
    def _get_data_size(self, conn: socket.socket) -> int:
        header = conn.recv(self.header_size)
        if not header:
            raise Exception("TODO")
        return struct.unpack('!I', header)[0]

    def _get_data(self, conn: socket.socket) -> bytearray:
        data = bytearray()
        remaining_size = self._get_data_size(conn)
        while remaining_size > 0:
            chunk = conn.recv(min(self.buffer_size, remaining_size))
            if not chunk:
                break
            data.extend(chunk)
            remaining_size -= len(chunk)
        return data
    
    def _send(
        self,
        conn: socket.socket,
        data: bytearray|bytes
    ):
        header = struct.pack('!I', len(data))
        conn.sendall(header)
        conn.sendall(data)
        
    
    def _error(
        self, 
        conn: Optional[socket.socket], 
        error_data: Optional[bytearray|bytes]
    ):
        if not error_data:
            return
        if not conn:
            return
        return self._send(conn, error_data)
    
    def _loop(self):
        conn = None
        try:
            conn, _ = self.socket.accept()
            data = self._get_data(conn)
            return_data = self.consumer.consume(data)
            if return_data:
                self._send(conn, return_data)
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
            