# Author: Alba Jano
# Last Modified: 23.02.2022

import socket
import tqdm
import os
import time

"""
Creating a communication server_socket:
Sources: 1) https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
         2) https://www.geeksforgeeks.org/socket-programming-python/
"""


class Server(object):
    def __init__(self, host="127.0.0.1", port=9990, filename=None):
        self.filesize = None
        self.socket = None
        self.filename = filename
        self.client_socket = None
        self.SERVER_HOST = host  # "192.168.56.1"  # device'server_socket IP address
        self.SERVER_PORT = port  # 80
        self.BUFFER_SIZE = 4096  # receive 4096 bits each time
        self.SEPARATOR = "<SEPARATOR>"
        self.TTI = 0
        self.ACK = "ACK"
        self.START_SIG = "START_SIG"
        self.START_SIG_ACK = "START_SIG_ACK"
        self.COMPLETION = "COMPLETION"
        self.file_received = False
        self.ack_sent = False

    def create_socket(self):
        # create the server server_socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[API Server][+] Socket successfully created")
        except socket.error as err:
            print("[API Server][-] Socket creation failed with error %s" % (err))
        # bind the server_socket to our local address
        self.socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        # enabling our server to accept connections; 5 here is the number of unaccepted connections that the system
        # will allow before refusing new connections
        self.socket.listen(5)
        print(f"[API Server][*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")

        # accept connection if there is any
        self.client_socket, address = self.socket.accept()
        # if below code is executed, that means the sender is connected
        print(f"[API Server][+] {address} is connected.")
        self.handshake()

    def handshake(self):
        dataFromClient = self.client_socket.recv(1024)
        received_dataClient = dataFromClient.decode()
        print("[API Server][+] Three way-handshake: Receiving %s" % (received_dataClient))
        if received_dataClient == self.START_SIG:
            print("[API Server][+] Three way-handshake: Sending " + self.START_SIG_ACK)
            self.client_socket.send(self.START_SIG_ACK.encode())
            dataFromClient = self.client_socket.recv(1024)
            received_dataClient = dataFromClient.decode()
            print("[API Server][+] Three way-handshake: Receiving %s" % (received_dataClient))
        else:
            return

    def receive_time_message(self):
        dataFromClient = self.client_socket.recv(1024)
        received_dataClient = dataFromClient.decode()
        print("[API Server][+] Time report: Receiving %s" % (received_dataClient))

    def receive_and_send_files(self):
        # receive the file infos
        # receive using client server_socket, not server server_socket
        # mec_simulation.receive_time_message()
        received = None
        while received is None or received == '':
            received = self.client_socket.recv(self.BUFFER_SIZE).decode()
            # print("RECEIVED : ")
            # print(received)
        self.client_socket.send(self.ACK.encode()) # Function moved to external side
        filename, filesize = received.split(self.SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the server_socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bits from the server_socket (receive)
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received; file transmitting is done
                    break
                elif bytes_read.decode() == self.COMPLETION:
                    bytes_read = None
                    f.close()
                    break
                # write to the file the bits we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        print("\n[API Server][+] Received file ")

        ###############################
        # File Processing Code
        ###############################

        self.dataFromServer = None
        self.filesize = os.path.getsize(self.filename)
        self.client_socket.send(f"{self.filename}{self.SEPARATOR}{self.filesize}".encode())
        while self.dataFromServer is None or self.dataFromServer == b'':
            try:
                time.sleep(0.1)
                self.dataFromServer = self.client_socket.recv(1024)
            except socket.error as err:
                print("[API Server][-] Data reception failed with %s" % (err))
        received_dataServer = self.dataFromServer.decode()
        if received_dataServer == self.ACK:
            # start sending the file
            progress = tqdm.tqdm(range(self.filesize), f"Sending {self.filename}", unit="B", unit_scale=True,
                                 unit_divisor=1024)
            bytes_read = None
            with open(self.filename, "rb") as f:
                while True:
                    # read the bits from the file
                    bytes_read = f.read(self.BUFFER_SIZE)
                    # progress.update(len(bytes_read))
                    if not bytes_read:
                        # file transmitting is done
                        self.client_socket.send(self.COMPLETION.encode())
                        break
                    self.client_socket.send(bytes_read)
                    time.sleep(0.1)
            progress.update(len(bytes_read)) # update the progress bar
            progress.close()

        print("[API Server][+] Sent file ")

    def send_ack(self):
        self.client_socket.send(self.ACK.encode())

    def close_socket(self):
        # close the client server_socket
        self.client_socket.close()
        # close the server server_socket
        self.socket.close()
        print("[API Server][+] Socket closed successfully")


if __name__ == '__main__':
    host = "127.0.0.1"  # "192.168.1.101"
    port = 9990  # 5001
    filename = "MEC.csv"
    server = Server(host, port, filename)
    server.create_socket()
    time.sleep(0.1)
    for _ in range(0, 20):
        server.receive_and_send_files()
    # server.close_socket()