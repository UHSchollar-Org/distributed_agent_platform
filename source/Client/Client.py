import socket
from utils import get_ip_port


def send_and_close(choice, message, socket: socket):
    socket.send(message.encode("utf-8"))
    data = socket.recv(1024)
    data = str(data.decode("utf-8"))
    if choice == "1" or choice == "3" or choice == "4":
        print(data)
    if choice == 2:
        print("The value corresponding to the key is : ", data)
    # socket.close()


def console():
    ip, port = get_ip_port()


    while True:
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. TO ENTER AGENT ***********************************")
        print("2. TO SHOW AGENT ************************************")
        print("3. TO DELETE ****************************************")
        print("4. TO USE AGENT *************************************")
        print("5. TO EXIT ******************************************")
        print("*****************************************************")

        choice = input()
        print("Estableciendo conexion: ", ip, port)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
            
        print("CHECK_0")
        
        if choice == "1":
            key = input("ENTER THE KEY: ")
            val = input("ENTER THE VALUE: ")
            message = "SET_AGENT|" + str(key) + ":" + str(val) + "\r\n"
            print("CHECK_1")
            send_and_close(choice, message, sock)
            print("CHECK_2")
            

        elif choice == "2":
            key = input("ENTER THE KEY: ")
            message = "GET_AGENT|" + str(key) + "\r\n"
            print("CHECK_1")
            send_and_close(choice, message, sock)
            print("CHECK_2")
            

        elif choice == "3":
            key = input("ENTER THE ID : KEY ")
            message = "delete|" + str(key)
            print("CHECK_1")
            send_and_close(choice, message, sock)
            print("CHECK_2")
            

        elif choice == "4":
            key = input("ENTER THE API NAME: ")
            message = "use_api|" + str(key)
            print("CHECK_1")
            send_and_close(choice, message, sock)
            print("CHECK_2")
            

        elif choice == "5":
            print("Closing the socket")
            print("CHECK_1")
            sock.close()
            print("CHECK_2")
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
