import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.15', 4270))
print('connected     going to close')
# time.sleep(5)
for i in range(1, 1000000):
    print(i)
print('sent')
client.send(b'aaa')
print('close now')
client.close()
print('closed')
