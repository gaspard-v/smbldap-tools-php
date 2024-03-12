from .linux.tcp import ServerBuilder, ConsumerAbstract
from .linux.signal import Signal

class Consumer(ConsumerAbstract):
    
    def __init__(self) -> None:
        self.signal = Signal()
        self.signal.capture()
    
    def consume(self, data: bytearray):
        decoded = data.decode()
        return print(f"decoded data: {decoded}")

    def stop_loop(self):
        return self.signal.stop_signal
        

def main():
    consumer = Consumer()
    server = ServerBuilder()
    server.create_socket().set_consumer(consumer).run()

if __name__ == "__main__":
    main()