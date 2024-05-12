def send_socket(client_socket, message):
    response = message + "\n"
    client_socket.send(response.encode('utf-8'))



def receive_socket(client_socket):
    client_socket.send("Enter: ".encode('utf-8'))
    data = client_socket.recv(1024)
    if not data:
        return None
    message = data.decode('utf-8', 'ignore').strip()
    return message


class CommunicationHandler:

    def __init__(self):
        self.clients = {}
        pass

    def add_client(self, client_socket, client_address):
        self.clients[client_address] = client_socket

    def remove_client(self, client_address):
        del self.clients[client_address]

    def broadcast(self, message):
        for client_address, client_socket in self.clients.items():
            send_socket(client_socket, message)
