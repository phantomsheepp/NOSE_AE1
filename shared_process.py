# Read file with given filename and send data over network via provided socket
def send_file(socket, filename):
    try:
        with open(filename,"rb") as file:
            data = file.read()
            socket.sendall(data)

    except Exception as e:
        print(e)

#  Create file with given filename and write to it data received via provided socket
def recv_file(socket, filename):
    try:
        file_contents = bytearray()
        data = socket.recv(4096)
        file_contents += data

        while len(data) > 0:
            data = socket.recv(4096)
            file_contents += data

        with open(filename,"xb") as file:
            file.write(file_contents)

    except Exception as e:
        print(e)

# Generate and send directory listing from server to client via provided socket
def send_listing(socket):
    try:
        dir_listing = os.listdir
        socket.sendall(dir_listing)

    except Exception as e:
            print(e)

# Recieve listing from server via provided socket and print it
def recv_listing(socket):
    try:
        dir_listing = socket.recv(4096)
        dir_listing = "\n".join(dir_listing)
        print(dir_listing)
    except Exception as e:
            print(e)
