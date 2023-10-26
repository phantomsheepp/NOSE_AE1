import socket
import sys
import os

sys.path.append('..')
from shared_process import send_file, recv_file
sys.path.append('server')
 

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    hostname = "0.0.0.0" #IP Address we were told to use in specification
    port = int(sys.argv[1])
    print(f"Server up and running on {hostname}:{port}")
    srv_sock.bind((hostname, port))

    srv_sock.listen(5) #the number is how many clients can interact with server (starting
    #with 0) not sure how many the specification actually wants, couldn't see anything

except Exception as e:
    # Print the exception message
    print(e)
    # Exit safely with error
    exit(1)

while True:
    try:
        cli_sock, cli_addr = srv_sock.accept()
        print(f"Client {cli_addr} connected.")

        data = cli_sock.recv(4096)

        choice_list = data.decode().split(" ")
        choice = str(choice_list[0])

        if choice == "list":
            # Retrieve directory contents and convert into correct format
            dir_contents_list = os.listdir()
            dir_contents_str = "\n".join(dir_contents_list)
            cli_sock.sendall(str.encode(dir_contents_str))

        elif choice == "get":
            filename = str(choice_list[1])
            if filename not in os.listdir():  #Check if file exists
                raise Exception("File not found")
            else:
                send_file(cli_sock, filename)
            
        elif choice == "put":
            filename = str(choice_list[1])
            
            if filename in os.listdir(): # Check if file exists
                raise Exception("File already exists")
            else:
                recv_file(cli_sock, filename)


    except Exception as e:
        print(e)  

    finally:
        cli_sock.close()

srv_sock.close()
exit(0)