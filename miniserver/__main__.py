from .linux.tcp import ServerBuilder
from .shadow import ShadowConsumer
        

def main():
    consumer = ShadowConsumer()
    server = ServerBuilder()
    server.create_socket().set_consumer(consumer).run()

if __name__ == "__main__":
    main()