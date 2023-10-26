import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file
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
    srv_sock.listen(5) #the number is how many clients can interact with server (starting
    #with 0) not sure how many the specification actually wants, couldn't see anything

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

        data = cli_sock.recv(4096)

        # Parse request
        choice_list = data.decode().split(" ")
        choice = str(choice_list[0])

        # Serve requests "list", "get", or "put" as given by client argument

        # "list" argument requests a list of first level directory contents
        if choice == "list":
            # Retrieve directory contents and convert into correct format
            dir_contents_list = os.listdir()
            dir_contents_str = "\n".join(dir_contents_list)
            cli_sock.sendall(str.encode(dir_contents_str))
            print(f"First level directory contents from the server {hostname}:{port} successfully returned to client.")

        # "get" argument downloads file
        elif choice == "get":
            filename = str(choice_list[1])

            # Check if file exists
            if filename not in os.listdir():  
                raise Exception(f"File {filename} failed to download from the server {hostname}:{port} as it was not found.")
            else:
                send_file(cli_sock, filename)
                print(f"File {filename} successfully downloaded from the server {hostname}:{port}.")

        # "put" argument uploads file
        elif choice == "put":
            filename = str(choice_list[1])

            # Check if file already exists
            if filename in os.listdir(): 
                raise Exception(f"File {filename} failed to upload to the server {hostname}:{port} as that file already exists.")
            else:
                recv_file(cli_sock, filename)
                print(f"File {filename} successfully uploaded to the server {hostname}:{port}.")


    # Catchall exception in case of larger error
    except Exception as e:
        print(e)  

    # Close client connection
    finally:
        cli_sock.close()

srv_sock.close()
exit(0)
