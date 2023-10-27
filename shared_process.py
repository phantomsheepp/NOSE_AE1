import os 

def valid_filename(name): 
    if "." not in name:
        print("No file extension found.")
        return False
    elif len(name) > 50:
        print("File name too long. Are you sure this is right?")
        return False
    
    return True


# Read file with given filename and send data over network via provided socket
def send_file(socket, filename, addr):
    try:
        with open(filename,"rb") as file:
            data = file.read()
            socket.sendall(data)

        print(f"File {filename} successfully sent to {addr}.")

    except BrokenPipeError:
        print(f"Connection broken to {addr} so send failed.")

    except Exception as e:
        print(e)
        print(f"File {filename} failed to send to {addr}.")


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
        print(f"Connection broken to {addr} so download failed.")

    except Exception as e:
        print(e)
        print(f"File {filename} failed to download from {addr}. Make sure the file exists.")


# Generate and send directory listing from server to client via provided socket
def send_listing(socket, addr):
    try:
        dir_contents_list = os.listdir()
        dir_contents_str = "\n".join(dir_contents_list)
        print(dir_contents_str)
        socket.sendall(str.encode(dir_contents_str))
        print(f"First level directory contents from the server successfully returned to client {addr}.")

    except Exception as e:
        print(e)
        print(f"First level directory contents from the server failed to send to client {addr}.")    

# Recieve listing from server via provided socket and print it
def recv_listing(socket, addr):
    try:
        data = socket.recv(4096)
        directory_list = data.decode()
        print("\nContents of directory: ")
        print(directory_list)
        print(f"\nFirst level directory contents from the server {addr} successfully returned to client.")

    except Exception as e:
        print(e)
        print(f"First level directory contents from the server failed to sent to client {addr}.")    
