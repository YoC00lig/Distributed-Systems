from socket import socket, timeout, AF_INET, SOCK_STREAM, SOCK_DGRAM, IPPROTO_UDP, inet_aton, IPPROTO_IP, IP_MULTICAST_TTL, IP_ADD_MEMBERSHIP, INADDR_ANY, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
from Constants import PINK,  RED, PICTURE_U, PICTURE_M, HOST, PORT, DEFAULT, ENCODING, BUFFER_SIZE, TIMEOUT_DURATION, MULTICAST_PORT, GROUP, TIME_TO_LIVE
from dataclasses import dataclass, field
import struct
import sys

@dataclass
class Client:
    socket: socket
    tcp_address: tuple
    udp_address: tuple = field(default=None)

class ChatClient:
    def __init__(self):
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)

    def connect_to_server(self):
        self.tcp_socket.connect((HOST, PORT))
        self.udp_socket.sendto(bytes(f'start_sending_udp_message {self.tcp_socket.getsockname()[1]}', ENCODING), (HOST, PORT))
        self.tcp_socket.settimeout(TIMEOUT_DURATION)
        self.udp_socket.settimeout(TIMEOUT_DURATION)

    def receive_tcp_messages(self):
        while True:
            try:
                if not (data := self.tcp_socket.recv(BUFFER_SIZE)): break
                message = data.decode(ENCODING).strip()
                print(f'{message}{PINK}')
            except timeout:
                pass
            except Exception as e:
                print(f"{RED}An error occurred while receiving TCP messages: {e}")
                break
        print(f'{RED}Disconnected from server.{DEFAULT}')

    def receive_udp_messages(self):
        while True:
            try:
                if not (data := self.udp_socket.recvfrom(BUFFER_SIZE)[0]): break
                print(DEFAULT, end='')
                print(data.decode(ENCODING), end='')
                print(PINK, end='\n')
            except timeout:
                pass
            except Exception as e:
                print(f"{RED}An error occurred while receiving UDP messages: {e}")
                break
        print(f'{RED}Disconnected from server.{DEFAULT}')

    def send_message(self):
        while True:
            try:
                message = input(PINK)
                print(DEFAULT, end='')
                if message == 'U':
                    self.udp_socket.sendto(f'send_picture {PICTURE_U}'.encode(ENCODING), (HOST, PORT))
                elif message == 'Q':
                    self.quit_chat()
                elif message == 'M':
                    self.send_multicast()
                elif message != '':
                    self.tcp_socket.sendall(message.encode(ENCODING))
            except Exception as e:
                print(f"{RED}An error occurred while sending message: {e}")
                break

    def send_multicast(self):  
        try:
            sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, TIME_TO_LIVE)
            sock.sendto(PICTURE_M.encode(ENCODING), (GROUP, MULTICAST_PORT))  
            print(f"{PINK}ASCII art picture sent via multicast.")
        except Exception as e:
            print(f"{RED}An error occurred while sending multicast message: {e}")

    def receive_multicast(self):
        sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((GROUP, MULTICAST_PORT))
        mreq = struct.pack("4sl", inet_aton(GROUP), INADDR_ANY)
        sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        while True:
            try:
                data, address = sock.recvfrom(BUFFER_SIZE)
                print(f"Received multicast message from {address}: {data.decode(ENCODING)}")
            except Exception as e:
                print(f"{RED}An error occurred while receiving multicast message: {e}")
                break

    def quit_chat(self):
        self.tcp_socket.close()
        self.udp_socket.close()
        sys.stdin.readline()
        sys.exit()

if __name__ == "__main__":
    client = ChatClient()
    client.connect_to_server()

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_tcp = executor.submit(client.receive_tcp_messages)
        future_udp = executor.submit(client.receive_udp_messages)
        future_multicast = executor.submit(client.receive_multicast)
        future_send = executor.submit(client.send_message)
        
        future_tcp.result()
        future_udp.result()
        future_multicast.result()
        future_send.result()

