import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.20.10.3', 4270))
print('connected     going to close')
client.send(bytes('', 'utf-8'))
time.sleep(1)
print('finished sleeping')
client.send(bytes('','utf-8'))
for i in range(1, 1000000):
    print(i)
print('finished loop')
client.send(b'')
print('close now')
client.close()
print('closed')
