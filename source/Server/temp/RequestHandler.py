import socket


# The class RequestHandler is used to manage all the requests for sending messages from one node to another
# the send_message function takes as the ip, port of the reciever and the message to be sent as the arguments and
# then sends the message to the desired node.
class RequestHandler:
    def __init__(self):
        pass

    def send_message(self, ip, port, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server on local computer
        s.connect((ip, port))
        s.send(message.encode("utf-8"))
        data = s.recv(1024)
        s.close()
        return data.decode("utf-8")
    
    def ping(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.sendall('\r\n'.encode('utf-8'))
            s.close()
            return True
        except socket.error:
            return False
