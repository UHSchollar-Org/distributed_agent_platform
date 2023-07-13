import socket
from xmlrpc.client import ProtocolError
from utils import get_ip_port, ping

IP, PORT = None, 9000
ips_ = [
    "192.168.191.1",
    "192.168.191.2",
    "192.168.191.3",
    "192.168.191.4",
    "192.168.191.5",
]


def send_and_close(choice, message, socket: socket.socket):
    socket.send(message.encode("utf-8"))
    data = socket.recv(1024)
    data = str(data.decode("utf-8"))
    if (
        choice == "1"
        or choice == "3"
        or choice == "4"
        or choice == "5"
        or choice == "6"
    ):
        print(data)
    if choice == "2":
        print("The value corresponding to the key is : ", data)
    socket.close()
    socket = None


def find_new_ip_port():
    print("RECONNECTING...")
    for ip in ips_:
        print("Iterating")
        if ping(ip, PORT):
            print(f"New ip {ip}, port {PORT}")
            return ip, PORT


def console():
    IP, PORT = get_ip_port()

    while True:
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. TO ENTER AGENT ***********************************")
        print("2. TO SHOW AGENT ************************************")
        print("3. TO DELETE ****************************************")
        print("4. TO USE AGENT *************************************")
        print("5. TO FIND AGENTS BY FUNCTIONALITY ******************")
        print("6. TO SHOW ALL AGENTS *******************************")
        print("7. TO EXIT ******************************************")
        print("*****************************************************")

        choice = input()

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            if choice != "7":
                print("Invalid choice")
                continue
            print("Exiting Client")
            exit()

        print("Estableciendo conexion: ", IP, PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((IP, PORT))
        except:
            IP, PORT = find_new_ip_port()
            # sock.connect((IP, PORT))
            sock.close()
            sock = None
            continue

        if sock.getpeername() == (IP, PORT):
            print("Conexión establecida con", sock.getpeername())
        else:
            print("Error al intentar establecer conexión")

        # insert
        if choice == "1":
            key = input("ENTER THE KEY: ")
            val = input("ENTER THE VALUE: ")
            message = "SET_AGENT|" + str(key) + ":" + str(val) + "\r\n"
            send_and_close(choice, message, sock)

        # get
        elif choice == "2":
            key = input("ENTER THE KEY: ")
            message = "GET_AGENT|" + str(key) + "\r\n"
            send_and_close(choice, message, sock)

        # delete
        elif choice == "3":
            key = input("ENTER THE AGENT NAME: ")
            id = input("ENTER THE AGENT ID: ")
            message = "DELETE|" + str(key) + ":" + str(id) + "\r\n"
            send_and_close(choice, message, sock)

        elif choice == "4":
            key = input("ENTER THE API_NAME ENPOIN_NAME PARMAS: ")
            message = "USE_AGENT|" + str(key) + "\r\n"
            send_and_close(choice, message, sock)

        elif choice == "5":
            key = input("ENTER FUNCTIONALITY ")
            message = "GET_FUNC|" + str(key) + "\r\n"
            send_and_close(choice, message, sock)

        elif choice == "6":
            message = "SHOW_ALL_AGENTS\r\n"
            print("SHOWING ALL AGENTS")
            send_and_close(choice, message, sock)


def main():
    console()


if __name__ == "__main__":
    main()
