import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(bytes('', 'utf-8'))
print('after send empty')
s.send(bytes('afterrrrrrr', 'utf-8'))
print('after send afterrrrrrr')
data = s.recv(100)
print('Received', data)
