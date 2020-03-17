import socket
import pickle
from ext import layer2Firewall
import constants
from sqlmanager import operationType
import pox.openflow.libopenflow_01 as of
import utilmethods
import pox.boot

bootCore = None

#TODO implement api handler here if connection object persists
#TODO remove debug statements

def initialize():
    global bootCore
    if bootCore == None:
        updateBootCore()
    print "initialize bootcore"
    print bootCore
    print bootCore.openflow.connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8000))
    try:
        server.listen(1)
        print "Server is listening on port " + str(8000)
        while True:
            clientConnection, addr = server.accept()
            print "Client Connected: " + str(addr)
            data = clientConnection.recv(4096)
            if data != None:
                formattedData = pickle.loads(data)
                apihandler(formattedData)
                clientConnection.sendall(pickle.dumps(getSuccessReponse()))
    except KeyboardInterrupt:
        server.close()
    except Exception as e:
        server.close()
        print e

def getSuccessReponse():
    return {"status":1}

def apihandler(data):
    #TODO check if the core object holds all the connections
    oType = data[constants.OTYPE]
    matchInstance = layer2Firewall.utilMethods.constructmatchStructure(utilmethods.extractAddress(data), data[constants.PROTO], data[constants.PORT])
    if oType == operationType[constants.INSERT]:
        for connection in bootCore.openflow.connections:
            msg = of.ofp_flow_mod()
            msg.match = matchInstance
            msg.command = of.OFPFC_ADD
            connection.send(msg)
    elif oType == operationType[constants.DELETE]:
        for connection in bootCore.openflow.connections:
            msg = of.ofp_flow_mod()
            msg.match = matchInstance
            msg.command = of.OFPFC_DELETE
            connection.send(msg)
    elif oType == operationType[constants.UPDATE]:
        for connection in bootCore.openflow.connections:
            # Delete the existing rule identified by the source and the destination address
            msg = of.ofp_flow_mod()
            msg.match = matchInstance
            msg.command = of.OFPFC_DELETE
            connection.send(msg)
    return data

def updateBootCore():
    print "Updating boot core"
    global bootCore
    bootCore = pox.boot.core




