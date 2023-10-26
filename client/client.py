import socket
import sys
import os
import time 

sys.path.append('..')
from shared_process import send_file, recv_file, recv_listing
sys.path.append('client')

# Create the client socket used to connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Parses arguments from the command line
hostname = str(sys.argv[1])
port = int(sys.argv[2])
choice = str(sys.argv[3])

srv_addr = (hostname, port) 

# Connect to server defined in command line 
try:
    cli_sock.connect(srv_addr)
    print(f"Client connected to server on {hostname}:{port}")

except Exception as e:
    print(e)
    exit(1)


# Construct and send request message, "list", "get", or "put"
try:

    # Request a list of first level directory contents
    if choice == "list":

        cli_sock.sendall(str.encode(choice))

        data = cli_sock.recv(4096)
        directory_list = data.decode()
        print("\nContents of directory: ")
        print(directory_list)
        print(f"\nFirst level directory contents from the server {hostname}:{port} successfully returned to client.")

        #recv_listing(cli_sock)


    # Request to download a file
    elif choice == "get":

        filename = sys.argv[4]

        # Check if file exists
        if filename in os.listdir():
            raise Exception(f"File {filename} failed to download from the server {hostname}:{port} as it already exists.")
        else:
            cli_sock.sendall(str.encode(f"{choice} {filename}"))
            time.sleep(1)
            recv_file(cli_sock, filename, srv_addr)
            
    # Request to upload a file
    elif choice == "put":

        filename = sys.argv[4]

        # Check if file already exists
        if filename not in os.listdir():
            raise Exception(f"File {filename} failed to upload to the server {hostname}:{port} as it was not found.")
        else:
            cli_sock.sendall(str.encode(f"{choice} {filename} "))
            send_file(cli_sock, filename, srv_addr)
            
# Catchall exception in case of larger error
except Exception as e:
    print(e)

# Close client connection
finally:
    cli_sock.close()

exit(0)
