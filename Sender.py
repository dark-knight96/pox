import socket
import pickle

def sendToServer(data):
    try:
        if type(data) != type({}):
            return -2 #incorrect data type
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 8000))
        client.sendall(pickle.dumps(data))
        incoming = client.recv(4096)
        response = pickle.loads(incoming)
        if response["status"] == 1:
            client.close()
            return 1
        else:
            return -1
    except:
        client.close()





