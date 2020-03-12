import socket
import pickle
from ext import layer2Firewall

#TODO implement api handler here if connection object persists

def initialize():
    from boot import core
    print core.openflow.connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8000))
    try:
        server.listen(1)
        print "Server is listening on port " + str(8000)
        while True:
            clientConnection, addr = server.accept()
            print "Client Connected: " + str(addr)
            data = clientConnection.recv(4096)
            formattedData = pickle.load(data)
            clientConnection.sendall(pickle.dumps(getSuccessReponse()))
    except KeyboardInterrupt:
        server.close()
    except Exception as e:
        server.close()
        print e

def getSuccessReponse():
    return {"status":1}

def apihandler(data):
    # Skeleton for apihandler
    #TODO check if the core object holds all the connections
    getCore = layer2Firewall.utilMethods.getCore()
    return data




