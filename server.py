import socket
from _thread import *

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 50100        # Port to listen on (non-privileged ports are > 1023)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(5)

def fun(clientsocket, address):
    print('Connected by', address)
    while True:
        try:
            data = clientsocket.recv(1024)
            if not data:
                break
            print('Received', repr(data))

        except:
            print('Disconnected!')
            return
    clientsocket.close()
    print('S-a terminat comunicarea cu ', address)

def run_server():
    while True:
        print('#########################################################################')
        print('Serverul asculta potentiali clienti.')
        print('#########################################################################')

        (conn, addr) = serversocket.accept()
        start_new_thread(fun, (conn, addr))
