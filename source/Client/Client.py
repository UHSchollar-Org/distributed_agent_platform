import socket


def main():
    # ip = input("Give the ip address of a node")
    ip = "127.0.0.1"
    # port = 9000
    port = int(input("Give the port number of a node: "))

    while True:
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. TO ENTER AGENT ***********************************")
        print("2. TO SHOW AGENTS ***********************************")
        print("3. TO DELETE ****************************************")
        print("4. TO USE AGENT *************************************")
        print("5. TO EXIT ******************************************")
        print("*****************************************************")
        choice = input()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((ip, port))

        if choice == "1":
            key = input("ENTER THE KEY: ")
            val = input("ENTER THE VALUE: ")
            message = "insert|" + str(key) + ":" + str(val)
            send_and_close(choice, message, sock)

        elif choice == "2":
            key = input("ENTER THE KEY: ")
            message = "search|" + str(key)
            send_and_close(choice, message, sock)

        elif choice == "3":
            key = input("ENTER THE ID : KEY ")
            message = "delete|" + str(key)
            send_and_close(choice, message, sock)

        elif choice == "4":
            key = input("ENTER THE API NAME: ")
            message = "use_api|" + str(key)
            send_and_close(choice, message, sock)

        elif choice == "5":
            print("Closing the socket")
            sock.close()
            print("Exiting Client")
            exit()

        else:
            print("INCORRECT CHOICE")


def send_and_close(choice, message, socket: socket):
    socket.send(message.encode("utf-8"))
    data = socket.recv(1024)
    data = str(data.decode("utf-8"))
    if choice == "1" or choice == "3" or choice == "4":
        print(data)
    if choice == 2:
        print("The value corresponding to the key is : ", data)
    socket.close()


if __name__ == "__main__":
    main()
