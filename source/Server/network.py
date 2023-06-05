import socket


# reads from socket until "\r\n"
def read_from_socket(socket):
    # yo anhadi lo del decode
    # donde dice data_decode era data
    result = ""
    while 1:
        data = socket.recv(256)
        data_decode = data.decode("utf-8")
        if data_decode[-2:] == "\r\n":
            result += data_decode[:-2]
            break
        result += data_decode
        # if result != "":
        #     print "read : %s" % result
    return result


# sends all on socket, adding "\r\n"
def send_to_socket(s, msg):
    #  "respond : %s" % msg
    tmp = msg + "\r\n"
    msg_ncode = tmp.encode("utf-8")
    s.sendall(msg_ncode)
