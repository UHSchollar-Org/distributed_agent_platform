import socket
from utils import get_ip_port


def send_and_close(choice, message, socket: socket):
    socket.send(message.encode("utf-8"))
    data = socket.recv(1024)
    data = str(data.decode("utf-8"))
    if choice == "1" or choice == "3" or choice == "4" or choice == "5":
        print(data)
    if choice == "2":
        print("The value corresponding to the key is : ", data)


def console():
    ip, port = get_ip_port()

    while True:
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. TO ENTER AGENT ***********************************")
        print("2. TO SHOW AGENT ************************************")
        print("3. TO DELETE ****************************************")
        print("4. TO USE AGENT *************************************")
        print("5. TO SHOW ALL AGENTS *******************************")
        print("6. TO EXIT ******************************************")
        print("*****************************************************")

        choice = input()
        print("Estableciendo conexion: ", ip, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

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
            key = input("ENTER THE API NAME: ")
            message = "USE_AGENT|" + str(key) + "\r\n"
            send_and_close(choice, message, sock)

        elif choice == "5":
            message = "SHOW_ALL_AGENTS\r\n"
            print("SHOWING ALL AGENTS")
            send_and_close(choice, message, sock)

        elif choice == "6":
            print("Closing the socket")
            sock.close()
            print("Exiting Client")
            exit()

        else:
            print("INCORRECT CHOICE")

        sock.close()
        sock = None


def main():
    console()


if __name__ == "__main__":
    main()
