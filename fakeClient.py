import socket

import time

client = socket.socket()
client.connect(('172.17.39.164', 4257))

# data = 'POST, teamNumber: 7476, compName: carleton, scoutTeam: 5024, auto: true, score: 100, bonusRP: true, climb: true, result: 2, totalRP:4'
# client.send(bytes(data, 'utf-8'))
# time.sleep(1)

data = 'GET, getCompetetions, teamNumber: 7476'
client.send(bytes(data, 'utf-8'))
time.sleep(1)

data = 'GET, getTeams, teamNumber: 7476, compName: carleton'
client.send(bytes(data, 'utf-8'))
time.sleep(1)

data = 'GET, getGeneralTeamInfo, teamNumber: 7476, compName: carleton, scoutTeam: 1111'
client.send(bytes(data, 'utf-8'))
time.sleep(1)

data = 'GET, getSpecificGameInfo, teamNumber: 7476, compName: carleton, scoutTeam: 1111, gameNum: 2'
client.send(bytes(data, 'utf-8'))
time.sleep(1)

data = 'BYE'
client.send(bytes(data, 'utf-8'))
time.sleep(1)

client.close()
