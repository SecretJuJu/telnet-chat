import socket
import threading

from client_handler import ClientHandler
from communication_handler import CommunicationHandler

# Max number of clients
max_client = 10


def main():
    communication_handler = CommunicationHandler()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 23))
    server_socket.listen(max_client)
    print('Server is listening for clients...')

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            communication_handler.add_client(client_socket, client_address)
            handler = ClientHandler(client_socket, client_address, communication_handler)

            thread = threading.Thread(target=handler.run)
            thread.start()
    except KeyboardInterrupt:
        print('Server shutting down...')
        server_socket.close()
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
