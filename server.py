import socket
import threading
import db

# print('alive threads', threading.activeCount(), threading.enumerate()
#       [0], threading.enumerate()[1], threading.enumerate()[2])

# alive threads 3
# <_MainThread(MainThread, started 4325809600)>
# <Thread(pymongo_server_monitor_thread, started daemon 123145438015488)>
# <Thread(pymongo_kill_cursors_thread, started daemon 123145443270656)>

port = 4257


class clientThreading(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        print('new connection from', self.addr)

    def run(self):
        try:
            while True:
                msg = self.client.recv(150).decode('utf-8')
                # print('==none', str(msg == None),
                #       '      == empty string ', str(msg == ''))
                if msg == '':
                    continue
                splitMsg = msg.split(',', 1)
                prefix = splitMsg[0]
                if prefix == 'BYE':
                    print('closing the client', self.addr)
                    self.client.close()
                    break
                elif prefix == 'POST':
                    data = splitMsg[1]
                    # data.replace('true', True)
                    # print(type(data),data)
                    data = data.replace(' ', '')
                    # print(data)
                    processed = data.split(',')
                    print('POST from', self.addr, processed)
                    result = db.recordGame( int(processed[0].split(':')[1]),
                                            processed[1].split(':')[1],
                                            int(processed[2].split(':')[1]),
                                            processed[3].split(':')[1] == 'true',
                                            int(processed[4].split(':')[1]),
                                            processed[5].split(':')[1] == 'true',
                                            processed[6].split(':')[1] == 'true',
                                            int(processed[7].split(':')[1]),
                                            int(processed[8].split(':')[1]))
                    print(result)
                    # teamNumber: 7476, compName: Carleton, scoutTeam: 5024, auto: true, score: 100, bonusRP: true, climb: true, result: 2, totalRP:4
                    # teamNumber, compName, scoutTeam, auto, score, bonusRP, climb, result, totalRP
                    # store data in db
                elif prefix == 'GET':
                    functionType = splitMsg[1].split(',', 1)[0].replace(' ', '')
                    data = splitMsg[1].split(',', 1)[1]
                    data = data.replace(' ', '')
                    processed = data.split(',')
                    print('GET from', self.addr, processed)
                    # print(functionType)
                    if functionType == 'getCompetetions':
                        result = db.getCompetetions(int(processed[0].split(':')[1]))
                        # print('result', db.getCompetetions(int(processed[0].split(':')[1])))
                    elif functionType == 'getTeams':
                        result = db.getTeams(int(processed[0].split(':')[1]), processed[1].split(':')[1])
                    elif functionType == 'getGeneralTeamInfo':
                        result = db.getGeneralTeamInfo( int(processed[0].split(':')[1]),
                                                        processed[1].split(':')[1],
                                                        int(processed[2].split(':')[1]))
                    elif functionType == 'getSpecificGameInfo':
                        result = db.getSpecificGameInfo(int(processed[0].split(':')[1]),
                                                        processed[1].split(':')[1],
                                                        int(processed[2].split(':')[1]),
                                                        int(processed[3].split(':')[1]))
                    
                    print(result)
                    # send data from db to android app
        except Exception as e:
            print(e)
            # this line might be problemactic since the connection is alrady closed by client
            self.client.close()
            print('client connection ends')


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print('server at', s.getsockname(), port)
s.close()


s = socket.socket()
s.bind(('0.0.0.0', port))

try:
    while True:
        print('alive threads     is here loop', threading.activeCount())
        s.listen(1)
        c, adr = s.accept()
        print('alive threads     after accept', threading.activeCount())
        clientThread = clientThreading(c, adr)
        clientThread.start()
except Exception as e:
    print(e)
    s.close()
    print('close server')
