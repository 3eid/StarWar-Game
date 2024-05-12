
from socket import *
from threading import *



def server_recieve(connection):
    while True:
        server_message=connection.recv(2048).decode()
        print(server_message)


client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8888))

client_thread = Thread(target=server_recieve,args=(client,))
client_thread.start()

while True:
    client.send(input().encode())
    