import threading
import socket

#server connection info
host = '192.168.1.30' #localhost
port = 1412 #port
print(host)

#creating server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected whit {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'{address} is using this name {nickname}')
        broadcast(f'{nickname} has joind the chat'.encode('ascii'))
        client.send('connected to the server sucsesfuly'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()