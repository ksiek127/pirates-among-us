import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "192.168.1.94"  # Asia
        self.server = "192.168.1.61"  # K
        # self.server = "192.168.1.102" # K 2
        self.port = 5555
        self.address = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(100000))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(100000))
        except socket.error as e:
            print(e)
