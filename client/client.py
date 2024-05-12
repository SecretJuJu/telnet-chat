import telnetlib
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox


class ChatClient:
    def __init__(self, master):
        self.telnet = None
        self.master = master
        master.title("Chat Client")

        # 채팅 로그를 표시하는 스크롤 가능한 텍스트 위젯
        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', height=20, width=50)
        self.chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # 메시지 입력 필드
        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.grid(row=1, column=0, padx=10, pady=10)
        self.msg_entry.bind("<Return>", self.send_message)  # 엔터키 바인딩

        # 메시지 전송 버튼
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.is_connected = False
        while not self.is_connected:
            self.connect_to_server()

    # 서버에 연결
    def connect_to_server(self):
        # 서버의 IP 주소와 포트 번호를 입력받음
        server_ip = simpledialog.askstring("Input", "Enter server IP address (default=127.0.0.1)", parent=self.master)
        server_port = simpledialog.askstring("Input", "Enter server port number (default=23)", parent=self.master)

        if not server_ip:
            server_ip = "127.0.0.1"
        if not server_port:
            server_port = 23

        server_port = int(server_port)

        if not server_ip or not server_port:
            messagebox.showerror("Error", "Invalid server IP address or port number")
            return

        # 서버에 연결
        try:
            self.telnet = telnetlib.Telnet(server_ip, server_port)
            self.is_connected = True
            self.update_chat_log("Connected to the server")
            threading.Thread(target=self.receive_message).start()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Could not connect to the server: {e}")
            self.is_connected = False

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            # 여기에 메시지를 서버로 보내는 코드를 추가
            self.telnet.write(msg.encode('utf-8') + b"\n")
            self.msg_entry.delete(0, tk.END)

    def update_chat_log(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

    def receive_message(self):
        while True:
            try:
                message = self.telnet.read_until(b"\n").decode('utf-8')
                if message:
                    self.update_chat_log(message.strip())
            except EOFError:
                self.update_chat_log("Connection closed by the server")
                break


def main():
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()


if __name__ == "__main__":
    main()
