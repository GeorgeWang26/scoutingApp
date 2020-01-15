import socket

import time

client = socket.socket()
client.connect(('192.168.0.15', 4270))

data = 'POST, teamNumber: 7476, compName: Carleton, scoutTeam: 5024, auto: true, score: 100, bonusRP: true, climb: true, result: 2, totalRP:4'
client.send(bytes(data, 'utf-8'))
recieve = client.recv(150).decode('utf-8')
while recieve == '':
    recieve = client.recv(150).decode('utf-8')
print(data, '\n' + recieve, '\n\n')


time.sleep(10)

data = 'GET, getCompetetions, teamNumber: 7476'
client.send(bytes(data, 'utf-8'))
recieve = client.recv(150).decode('utf-8')
while recieve == '':
    recieve = client.recv(150).decode('utf-8')
print(data, '\n' + recieve, '\n\n')

data = 'GET, getTeams, teamNumber: 7476, compName: carleton'
client.send(bytes(data, 'utf-8'))
recieve = client.recv(150).decode('utf-8')
while recieve == '':
    recieve = client.recv(150).decode('utf-8')
print(data, '\n' + recieve, '\n\n')

data = 'GET, getGeneralTeamInfo, teamNumber: 7476, compName: carleton, scoutTeam: 5024'
client.send(bytes(data, 'utf-8'))
recieve = client.recv(150).decode('utf-8')
while recieve == '':
    recieve = client.recv(150).decode('utf-8')
print(data, '\n' + recieve, '\n\n')

data = 'GET, getSpecificGameInfo, teamNumber: 7476, compName: carleton, scoutTeam: 5024, gameNum: 2'
client.send(bytes(data, 'utf-8'))
recieve = client.recv(150).decode('utf-8')
while recieve == '':
    recieve = client.recv(150).decode('utf-8')
print(data, '\n' + recieve, '\n\n')

# data = 'BYE'
# client.send(bytes(data, 'utf-8'))

client.close()
