import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file, recv_listing, valid_filename, status_message
sys.path.append('client')


############# CONNECTION TO SERVER #############


# Create the client socket used to connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Parses arguments from the command line
    hostname = str(sys.argv[1])
    port = int(sys.argv[2])
    choice = str(sys.argv[3])

    # Checks for valid choice input
    if choice not in ["list", "get", "put"]:
        raise Exception("Failure -> Error: Request not valid - please input list, get, or put.")

    # Performs specific file name relevant checks
    if (choice in ["get", "put"]):
        if (len(sys.argv) != 5):
            raise IndexError("Failure -> Error: No file name given.")
        
        filename = sys.argv[4]
        if not valid_filename(filename)[0]:
            raise Exception(f"Failure -> Error: {valid_filename(filename)[1]}")

    # Connect to server defined in command line 
    srv_addr = (hostname, port)
    cli_sock.connect(srv_addr)
    print(f"Client connected to server on {hostname}:{port}") 

except Exception as e:
    print(f"Failure -> Error: {e}")
    exit(1)


############# REQUEST PROCESSING #############


# Construct and send request message: "list", "get", or "put"
try:

    # Request a list of first level directory contents
    if choice == "list":
        cli_sock.sendall(str.encode(choice))

        dir_list_status = recv_listing(cli_sock, srv_addr)
        if dir_list_status[0]:
            cli_sock.sendall(str.encode("Success,"))
            print(status_message("Success", srv_addr, choice))
        else:
            cli_sock.sendall(str.encode(f"Failure,{dir_list_status[1]}"))

    # Request to download a file
    elif choice == "get":
        
        # Sends request to server
        cli_sock.sendall(str.encode(f"{choice} {filename} "))

        # Checks if file already exists in client directory
        if filename in os.listdir():
            cli_sock.sendall(str.encode(f"Failure,File already exists in client directory."))
            raise Exception(status_message("Failure", srv_addr, choice, filename, "File already exists in client directory."))
        
        # Sends go ahead to server to start processing request
        cli_sock.sendall(str.encode("Success,"))

        # Recevies whether or not file exists in server directory
        server_status = (cli_sock.recv(1024).decode()).split(",")
        if server_status[0] == "Failure":
            raise Exception(status_message("Failure", srv_addr, choice, filename, server_status[1]))
        
        # Checks if receive was successful and informs server
        recv_status = recv_file(cli_sock, filename, srv_addr)
        if recv_status[0]:
            cli_sock.sendall(str.encode("Success,"))
            print(status_message("Success", srv_addr, choice, filename))
        else:
            cli_sock.sendall(str.encode(f"Failure,{recv_status[1]}"))
            raise Exception(status_message("Failure", srv_addr, choice, filename, recv_status[1]))
        

    # Request to upload a file
    elif choice == "put":

        # Sends request to server
        cli_sock.sendall(str.encode(f"{choice} {filename} "))

        # Check if file exists in client directory
        if filename not in os.listdir():
            cli_sock.sendall(str.encode("Failure,File does not exist in client directory."))
            raise Exception(status_message("Failure", srv_addr, choice, filename, "File does not exist in client directory."))
        
        # Sends go ahead to server to start processing request
        cli_sock.sendall(str.encode("Success,"))

        # Checks if file already exists in server directory
        server_status = (cli_sock.recv(1024).decode()).split(",")
        if server_status[0] == "Failure":
            raise Exception(status_message("Failure", srv_addr, choice, filename, server_status[1]))
        
        # Checks if send was successful
        send_status = send_file(cli_sock, filename, srv_addr)
        if not send_status[0]:
            raise Exception(status_message("Failure", srv_addr, choice, filename, send_status[1]))

        # Checks that the server has successfully recevied file
        server_status = (cli_sock.recv(1024).decode()).split(",")
        if server_status[0]:
            print(status_message("Success", srv_addr, choice, filename))
        else:
            print(status_message("Failure", srv_addr, choice, filename, server_status[1]))

except Exception as e:
    print(e)

# Closes client connection 
finally:
    cli_sock.close()

exit(0)
