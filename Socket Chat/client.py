import socket
import threading
from termcolor import colored
import colorama
import sys

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.ADDR = (ip, port)
        self.DISCONNECT_MESSAGE = "close"
        self.FORMAT = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True
        # self.nickname = input("Enter your nickname: ")
        self.nickname = "Admin"
    def receive(self):
        while self.connected:
            message = self.client.recv(2048).decode(self.FORMAT)
            if message:
                return message
            else:
                continue
    def write(self, message):
        self.client.send(message.encode(self.FORMAT))
    def sendFile(self, message):
        self.client.send(message)
    def recFile(self):
        while self.connected:
            message = self.client.recv(1024)
            if message:
                return message
            else:
                continue
    def connect(self):
        try:
            self.client.connect(self.ADDR)
        except:
            self.connected = False
    def close(self):
        self.client.close()



