from Constants import DEFAULT, BLUE, RED, GREEN, ENCODING, WELCOME_MESSAGE, CLIENT_JOIN_MESSAGE
from socket import socket

class Messenger:
    @staticmethod
    def broadcast_message(sender: str, message: str, sender_address: tuple, clients: list):
        formatted_message = f'{BLUE}>{DEFAULT} {sender}: {message}' if sender != 'Server' else f'{DEFAULT}{message}'
        for client in clients:
            if client.tcp_address != sender_address:
                client.socket.sendall(formatted_message.encode(ENCODING))

    @staticmethod
    def send_welcome_message(client_socket: socket):
        client_socket.sendall(WELCOME_MESSAGE.encode(ENCODING))

    @staticmethod
    def broadcast_client_join_message(nickname : str, client_address : tuple, clients: list, client_socket : socket):
        print(GREEN, f'{nickname} {client_address} has joined the chat')
        Messenger.broadcast_message('', f'{GREEN}{nickname} has joined the chat', client_address, clients)
        client_socket.sendall(CLIENT_JOIN_MESSAGE.encode(ENCODING))

    @staticmethod
    def broadcast_client_leave_message(nickname : str, client_address : tuple, clients: list):
        print(RED, f'{nickname} {client_address} has left the chat')
        Messenger.broadcast_message('', f'{RED}{nickname} has left the chat', client_address, clients)