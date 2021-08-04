import json
import socket
import sys
import threading
import time

import matplotlib.pyplot as plt
import numpy as np


class ClientHandler(threading.Thread):
    def __init__(self, address, clientsocket, clients):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.address = address
        self.clientsocket = clientsocket
        self.clients = clients

    def run(self):
        print(f"[NEW CONNECTION] {self.address} connected.")

        while not self.shutdown_flag.is_set():
            try:
                data = self.clientsocket.recv(16)
                if len(data) == 0:
                    break
            except BlockingIOError:
                pass
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Socket error {e}")
                break

            time.sleep(0.5)

        print(f"Socket for {self.address} has been disconnected")
        index = self.clients.index(self.clientsocket)
        del self.clients[index]


class SocketHandler(threading.Thread):
    def __init__(self, clients):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.clients = clients

    def run(self):
        PORT = 1300
        # SERVER = socket.gethostbyname(socket.gethostname())
        SERVER = "localhost"
        ADDR = (SERVER, PORT)

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(ADDR)
        except:
            print(f"[Error] Port- {PORT} cannot connect as a socket")

        server.listen(5)
        threads = []
        print(f"[Connection] Port- {PORT} open to connect")

        while not self.shutdown_flag.is_set():
            clientsocket, address = server.accept()
            clientsocket.setblocking(0)
            self.clients.append(clientsocket)
            print(f"Connection from {address} has been established")

            clientThread = ClientHandler(address, clientsocket, self.clients)
            clientThread.daemon = True
            clientThread.start()
            threads.append(clientThread)
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")

        for t in threads:
            t.shutdown_flag.set()


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """

    # print("[EXCEPTION] exception raised", e)

    pass
