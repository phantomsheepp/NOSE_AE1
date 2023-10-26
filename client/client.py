import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file
sys.path.append('server')

# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
hostname = str(sys.argv[1])
port = int(sys.argv[2])
choice = str(sys.argv[3])

srv_addr = (hostname, port) 

try:
    print(f"Client connected to server on {hostname}:{port}")
    cli_sock.connect(srv_addr)

except Exception as e:
    print(e)
    exit(1)


try:

    if choice == "list":

        cli_sock.sendall(str.encode(choice))

        data = cli_sock.recv(1024)
        directory_list = data.decode()
        print("\nContents of directory: ")
        print(directory_list)

    elif choice == "get":

        filename = sys.argv[4]
        if filename in os.listdir():
            raise Exception("File already exists")
        else:
            cli_sock.sendall(str.encode(f"{choice} {filename}"))
            recv_file(cli_sock, filename)

    elif choice == "put":

        filename = sys.argv[4]
        print(filename)
        if filename not in os.listdir():
            raise Exception("File doesn't exist")
        else:
            cli_sock.sendall(str.encode(f"{choice} {filename} "))
            send_file(cli_sock, filename)

except Exception as e:
    print(e)

finally:
    cli_sock.close()

exit(0)