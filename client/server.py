import socket
import sys

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = "0.0.0.0" #IP Address we were told to use in specification
port = sys.argv[0]

cli_sock.bind((hostname, port))

cli_sock.listen(10) #the number is how many clients can interact with server (starting
#with 0) not sure how many the specification actually wants, couldn't see anything

print(f"Server up and running on {hostname}:{port}")

cli_socket, cli_address = cli_sock.accept()

#this is the first paragraph before things get goofy and hard. will 
#send you link to website where I got info. seems pretty solid, although
#idk if we want stuff in function or not, the examples seem to have this 
#stuff not in one though soooooo