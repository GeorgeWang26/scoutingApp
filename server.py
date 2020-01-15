import socket
import threading
import db

PORT = 4270
threadList = []


# print('alive threads', threading.activeCount(), threading.enumerate()[0], threading.enumerate()[1], threading.enumerate()[2])

# alive threads 3
# <_MainThread(MainThread, started 4325809600)>
# <Thread(pymongo_server_monitor_thread, started daemon 123145438015488)>
# <Thread(pymongo_kill_cursors_thread, started daemon 123145443270656)>


class clientThreading(threading.Thread):

    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        self.terminate = False
        print('new connection from', self.addr)

    def run(self):
        try:
            while True:
                if self.terminate:
                    # self terminate
                    break
                msg = self.client.recv(150).decode('utf-8')
                if not msg:
                    # terminate by client, socket will recv b'', decode into ''
                    break
                print(msg)
                msg = msg.replace(' ', '')
                splitMsg = msg.split(',', 1)
                prefix = splitMsg[0]
                info = splitMsg[1]
                result = ''

                if prefix == 'POST':
                    # clinet send data to store in server
                    data = info
                    processed = data.split(',')
                    print('POST from', self.addr, processed)
                    # store data in db 
                    result = db.recordGame( int(processed[0].split(':')[1]),
                                            processed[1].split(':')[1],
                                            int(processed[2].split(':')[1]),
                                            processed[3].split(':')[1] == 'true',
                                            int(processed[4].split(':')[1]),
                                            processed[5].split(':')[1] == 'true',
                                            processed[6].split(':')[1] == 'true',
                                            int(processed[7].split(':')[1]),
                                            int(processed[8].split(':')[1]))

                elif prefix == 'GET':
                    # client asking server to send data over
                    functionType = info.split(',', 1)[0]
                    data = info.split(',', 1)[1]
                    processed = data.split(',')
                    print('GET from', self.addr, processed)

                    # get data from db
                    if functionType == 'getCompetetions':
                        result = db.getCompetetions(int(processed[0].split(':')[1]))

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

                if result == '':
                    result = 'not found'
                print(result)
                self.client.send(bytes(result, 'utf-8'))
                
        except Exception as e:
            print('in thread exception\n', e)


        self.terminate = True
        self.client.close()
        print('client connection ended', self.addr, '\n')
        print('alive threads after closing current thread', threading.activeCount() - 3 - 1)
        print('before', threadList)
        removeFromThreads(self)
        print('after', threadList)
        print(threadList, '\n')





def terminateAllThreads():
    print('terminating', len(threadList), threadList)
    i = 1
    for thread in threadList:
        print(i, type(thread), thread)
        thread.terminate = True
        print('closed', i,'\n\n')
        i += 1
    print('all threads terminated')

def removeFromThreads(current):
    i = 0
    for thread in threadList:
        if thread == current:
            threadList.pop(i)
            

if __name__ == '__main__':
    # TCP can't get its IP?
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(("8.8.8.8", 80))
    # print('server at', PORT)
    # s.close()


    s = socket.socket()
    s.bind(('0.0.0.0', PORT))
    print('server started at', PORT)


    try:
        while True:
            print('alive threads before new connection', threading.activeCount() - 3)
            print(threadList, '\n')
            # allows 10 interruptions before declining new connections
            # since more than one clinet could be opening the app the same time
            s.listen(10)
            client, addr = s.accept()
            clientThread = clientThreading(client, addr)
            clientThread.start()
            threadList.append(clientThread)
    except KeyboardInterrupt as e:
        # self terminate
        s.close()
        print('server closed\n\n')
        terminateAllThreads()
        print('\n\nclosed')