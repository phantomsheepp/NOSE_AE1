import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file, send_listing, status_message
sys.path.append('server')
 

############# CONNECTION TO SERVER #############


# Creating TCP server socket
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try:
    # "0.0.0.0" used as means all IP addresses so we can recieve messages at port number on all interfaces/addresses
    hostname = "0.0.0.0"

    # Takes the port argument from the command line
    port = int(sys.argv[1])
 
    # Binds server to user defined port number
    srv_sock.bind((hostname, port))

    print(f"Server up and running on {hostname}:{port}")

    # Waits for client connections
    srv_sock.listen(5) 
    
except Exception as e:
    # Prints exception message and exits safely
    print(f"Failure -> Error: {e}")
    exit(1)


############# REQUEST PROCESSING #############


while True:
    try:
        # Connect client's socket and address to server
        cli_sock, cli_addr = srv_sock.accept()
        print(f"Client {cli_addr} connected.")

        # Receives client's request
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

        if choice in ["get", "put"]:
            filename = str(choice_list[1])

        # Serve requests "list", "get", or "put" as given by client argument

        # "list" argument requests a list of first level directory contents
        if choice == "list":
            send_listing(cli_sock, cli_addr)

            # Check that client successfully received directory list
            client_status = (cli_sock.recv(1024).decode()).split(",")
            if client_status[0] == "Success":
                print(status_message("Success", cli_addr, choice))
            else:
                print(status_message("Failure", cli_addr, choice, client_status[1]))


        # "get" argument downloads file
        elif choice == "get":

            # Receives whether or not file already exists in client directory
            client_status = (cli_sock.recv(1024).decode()).split(",")
            if client_status[0] == "Failure":
                raise Exception(status_message("Failure", cli_addr, choice, filename, client_status[1]))

            # Checks if file exists in server directory
            if filename not in os.listdir():  
                cli_sock.sendall(str.encode("Failure,File does not exist in server directory."))
                raise Exception(status_message("Failure", cli_addr, choice, filename, "File does not exist in server directory."))
            
            # Sends go ahead to client to 
            cli_sock.sendall(str.encode("Success,"))

            # Checks if send was successful
            send_status = send_file(cli_sock, filename, cli_addr)
            if not send_status[0]:
                raise Exception(status_message("Failure", cli_addr, choice, filename, send_status[1]))

            # Checks that client has successfully received file
            client_status = (cli_sock.recv(1024).decode()).split(",")
            if client_status[0] == "Success":
                print(status_message("Success", cli_addr, choice, filename))
            else:
                print(status_message("Failure", cli_addr, choice, filename, client_status[1]))


        # "put" argument uploads file
        elif choice == "put":

            # Receives whether or not file exists in client directory
            client_status = (cli_sock.recv(1024).decode()).split(",")
            if client_status[0] == "Failure":
                raise Exception(status_message("Failure", cli_addr, choice, filename, client_status[1]))

            # Check if file already exists in server directory
            if filename in os.listdir(): 
                cli_sock.sendall(str.encode(("Failure,File already exists in the server directory.")))
                raise Exception(status_message("Failure", cli_addr, choice, filename, "File already exists in server directory."))

            # Sends go ahead to client to send file
            cli_sock.sendall(str.encode("Success,"))

            # Checks if receive was successful and informs client
            recv_status = recv_file(cli_sock, filename, cli_addr)
            if recv_status[0]:
                cli_sock.sendall(str.encode("Success,"))
                print(status_message("Success", cli_addr, choice, filename))
            else:
                cli_sock.sendall(str.encode(f"Failure,{recv_status[1]}"))
                raise Exception(status_message("Failure", cli_addr, choice, filename, recv_status[1]))

    except Exception as e:
        print(e)  

    # Closes client connection
    finally:
        # Ensures a client socket exists before closing it
        if "cli_sock" in locals():
            cli_sock.close()

srv_sock.close()
exit(0)
