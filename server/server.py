import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file, send_listing
sys.path.append('server')
 
# Creating TCP server socket
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 



try:

    # "0.0.0.0" used as means all IP addresses so we can recieve messages at port number on all interfaces/addresses
    hostname = "0.0.0.0"

    # Take the port argument from the command line
    port = int(sys.argv[1])
 
    # Bind server to user defined port number
    srv_sock.bind((hostname, port))

    # Report success
    print(f"Server up and running on {hostname}:{port}")

    # Wait for client connections
    srv_sock.listen(5) 
    
except Exception as e:
    # Print the exception message
    print(e)
    # Exit safely with error
    exit(1)

while True:
    try:
        # Connect client's socket and address to server
        cli_sock, cli_addr = srv_sock.accept()
        print(f"Client {cli_addr} connected.")

        client_data = bytearray()
        while True:
            data = cli_sock.recv(1024)
            if data: 
                client_data += data
            if not data or len(data) < 1024:
                break

        # Parse request
        choice_list = client_data.decode().split(" ")
        choice = str(choice_list[0])
        print(choice_list)

        if choice in ["get", "put"]:
            filename = str(choice_list[1])

            file_contents = "".join(choice[2:])
            print("yuh"+file_contents)

        # Serve requests "list", "get", or "put" as given by client argument

        # "list" argument requests a list of first level directory contents
        if choice == "list":
            send_listing(cli_sock, cli_addr)

        # "get" argument downloads file
        elif choice == "get":
            filename = str(choice_list[1])

            # Check if file exists
            if filename not in os.listdir():  
                raise Exception(f"File {filename} failed to send to the client {cli_addr} as it was not found.")
            else:
                send_file(cli_sock, filename, cli_addr)
                print(f"File {filename} successfully sent to the client {cli_addr}.")

        # "put" argument uploads file
        elif choice == "put":
            filename = str(choice_list[1])

            # Check if file already exists
            if filename in os.listdir(): 
                raise Exception(f"File {filename} failed to download from the client {cli_addr} as that file already exists.")
            else:
                recv_file(cli_sock, filename, cli_addr)
                print(f"File {filename} successfully download to the server {hostname}:{port}.")


    # Catchall exception in case of larger error
    except Exception as e:
        print(e)  

    # Close client connection
    finally:
        # Ensures a client socket exists before closing it
        if "cli_sock" in locals():
            cli_sock.close()

srv_sock.close()
exit(0)
