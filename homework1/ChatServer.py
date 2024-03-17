from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import sleep
from Constants import DEFAULT, HOST, PORT, ENCODING, BUFFER_SIZE, RED
from Messenger import Messenger
from ChatClient import Client

class ChatServer:
    def __init__(self):
        self.tcp = socket(AF_INET, SOCK_STREAM)
        self.udp = socket(AF_INET, SOCK_DGRAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.tcp.bind((HOST, PORT))
        self.udp.bind((HOST, PORT))
        self.tcp.listen()

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(self.listen_tcp_message, executor)
            executor.submit(self.listen_udp_message)
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                self.close_clients_connections_and_sockets()

    def listen_tcp_message(self, executor: ThreadPoolExecutor):
        while True:
            try:
                client_socket, tcp_address = self.tcp.accept()
                self.clients.append(Client(socket=client_socket, tcp_address=tcp_address))
                executor.submit(self.handle_client_connection, client_socket, tcp_address)
            except Exception as e:
                print(f"{RED}An error while listening TCP occurred: {e}")
                break

    def handle_nickname_choosing(self, client_socket: socket):
        while True:
            nickname = client_socket.recv(BUFFER_SIZE).decode(ENCODING).strip()
            if nickname in self.nicknames:
                message = f'{DEFAULT}Chosen nickname is already in use. Choose a different nickname: '.encode(ENCODING)
                client_socket.sendall(message)
            elif not nickname:
                client_socket.sendall(f'{DEFAULT} Choose your nickname: '.encode(ENCODING))
            else:
                self.nicknames.append(nickname)
                return nickname

    def handle_client_connection(self, client_socket: socket, client_address: tuple):
        Messenger.send_welcome_message(client_socket)
        nickname = self.handle_nickname_choosing(client_socket)
        Messenger.broadcast_client_join_message(nickname, client_address, self.clients, client_socket)

        while True:
            if not (data := client_socket.recv(BUFFER_SIZE)) or not (message := data.decode(ENCODING).strip()): break
            elif message == 'Q': break
            else: Messenger.broadcast_message(nickname, message, client_address, self.clients)
            
        self.handle_client_leave(nickname, client_address, client_socket)

    def listen_udp_message(self):
        while True:
            try:
                buffer, udp_address = self.udp.recvfrom(BUFFER_SIZE)
                message_type, message = buffer.decode(ENCODING).split(' ', 1)
                if message_type == 'start_sending_udp_message':
                    self.handle_init_udp_message(message, udp_address)
                elif message_type == 'send_picture':
                    self.handle_udp_message(message, udp_address)
            except Exception as e:
                print(f"{RED}An error while listening UDP occurred: {e}")
                break

    def handle_init_udp_message(self, message, udp_address):
        tcp_port = int(message)
        for client in self.clients:
            if client.tcp_address[1] == tcp_port:
                client.udp_address = udp_address
                break

    def handle_udp_message(self, message, udp_address):
        for client in self.clients:
            if client.udp_address != udp_address:
                self.udp.sendto(message.encode(ENCODING), client.udp_address)

    def close_clients_connections_and_sockets(self):
        for client in self.clients:
            client.socket.close()
        self.clients.clear()
        self.tcp.close()
        self.udp.close()

    def close_client_connection(self, client_socket: socket):
        for client in self.clients:
            if client.socket == client_socket:
                client.socket.close()
                self.clients.remove(client)
                break

    def handle_client_leave(self, nickname, client_address : tuple, client_socket: socket):
        self.close_client_connection(client_socket)
        self.nicknames.remove(nickname)
        Messenger.broadcast_client_leave_message(nickname, client_address, self.clients)

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
