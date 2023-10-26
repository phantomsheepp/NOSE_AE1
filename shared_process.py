def send_file(socket, filename):
    try:
        with open(filename,"rb") as file:
            data = file.read()
            socket.sendall(data)

    except Exception as e:
        print(e)


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

# def send_listing(socket):
        
# def recv_listing(socket):