from random import randrange

from communication_handler import send_socket, receive_socket


def generate_emoji():
    return chr(randrange(128512, 128591))


class ClientHandler:
    def __init__(self, client_socket, addr, communication_handler):
        self.emoji = None
        self.is_init = None
        self.nickname = None
        self._nickname = None
        self.colored_nickname = None
        self.client_socket = client_socket
        self.addr = addr
        self.communication_handler = communication_handler

    def colored_nickname(self):
        return

    def set_nickname(self, nickname):
        self._nickname = nickname
        self.emoji = generate_emoji()
        self.nickname = f"{self.emoji} {nickname}"

    def run(self):
        print(f"[+] New connection from {self.addr}")
        try:
            while True:
                if not self.is_init:
                    send_socket(self.client_socket, "Type \"Start\" to begin, or \"exit\" to leave the chat")
                    message = receive_socket(self.client_socket)
                    if message == "Start":
                        send_socket(self.client_socket, "Enter your nickname")
                        nickname = receive_socket(self.client_socket)
                        self.set_nickname(nickname)
                        self.is_init = True
                        send_socket(self.client_socket, f"Welcome {self.nickname}")
                    else:
                        send_socket(self.client_socket, "Invalid command")
                        continue

                message = receive_socket(self.client_socket)

                if message == "exit":
                    break

                # filtering out empty messages and messages that are only spaces
                if not message or not message.strip():
                    continue

                # color apply in terminal & color is only for nickname
                self.communication_handler.broadcast(f"[{self.nickname}]: {message}")
        except ConnectionResetError:
            print(f"[-] Connection reset from {self.addr}")
        finally:
            self.client_socket.close()
            self.communication_handler.remove_client(self.addr)
            self.communication_handler.broadcast(f"[-] {self.nickname} has left the chat")
            print(f"[-] Connection closed from {self.addr}")
