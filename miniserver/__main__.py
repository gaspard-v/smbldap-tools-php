from .linux.tcp import ServerBuilder, ConsumerAbstract

class Consumer(ConsumerAbstract):
    
    def consume(self, data: bytearray):
        decoded = data.decode()
        return print(f"decoded data: {decoded}")
        

def main():
    consumer = Consumer()
    server = ServerBuilder()
    server.create_socket().set_consumer(consumer).run()

if __name__ == "__main__":
    main()