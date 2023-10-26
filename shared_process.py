import os 

# Read file with given filename and send data over network via provided socket
def send_file(socket, filename, addr):
    try:
        with open(filename,"rb") as file:
            data = file.read()
            socket.sendall(data)

        print(f"File {filename} successfully uploaded to {addr}.")

    except BrokenPipeError:
        print(f"Connection broken to {addr} so upload failed.")

    except Exception as e:
        print(e)
        print(f"File {filename} failed to upload to {addr}.")


# Create file with given filename and write to it data received via provided socket
def recv_file(socket, filename, addr):
    try:
        file_contents = bytearray()
        data = socket.recv(4096)
        file_contents += data

        while len(data) > 0:
            data = socket.recv(4096)
            file_contents += data

        with open(filename,"xb") as file:
            file.write(file_contents)

        print(f"File {filename} successfully downloaded from {addr}.")

    except BrokenPipeError:
        print(f"Connection broken to {addr}.")

    except Exception as e:
        print(e)
        print(f"File {filename} failed to download from {addr}.")


def receive_data(socket, addr):
    try:
        """file_contents = bytearray()
        data = socket.recv(4096)
        file_contents += data

        while len(data) > 0:
            data = socket.recv(4096)
            file_contents += data"""

        received_data = bytearray()

        print("HI")
        while True: 
            print("NO")
            data = socket.recv(4096)
            print("WADDUOP")
            print(data)

            if not data:
                break

            received_data += data
        
        return received_data
        
    
    except BrokenPipeError:
        print(f"Connection broken to {addr}.")

    except Exception as e:
        print(e)
        print(f"Failed to receive data.")

    return None
        

# Generate and send directory listing from server to client via provided socket
def send_listing(socket, addr):
    try:
        dir_contents_list = os.listdir()
        dir_contents_str = "\n".join(dir_contents_list)
        socket.sendall(str.encode(dir_contents_str))
        print(f"First level directory contents from the server successfully returned to client {addr}.")


    except Exception as e:
        print(e)
        print(f"First level directory contents from the server unsuccessfully sent to client {addr}.")    

# Recieve listing from server via provided socket and print it
def recv_listing(socket):
    try:
        dir_listing = socket.recv(4096)
        dir_listing = "\n".join(dir_listing)
        print("\nContents of directory: ")
        print(dir_listing)
        print(f"\nFirst level directory contents from the server {hostname}:{port} successfully returned to client.")

    except Exception as e:
            print(e)
