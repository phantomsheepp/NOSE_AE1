import os 

# Delimiter for the end of file and directory transfers
DELIMITER = b"#END#"

def valid_filename(name): 
    """Ensures a valid file name has been inputted"""

    if "." not in name:
        return (False,"No file extension found.")
    
    return (True,"")

def status_message(status, addr, type, filename="", error=""): 
    """Generates standardly formatted status messages to describe the result of a request"""

    if type == "list":
        if error == "":
            return f"{status} for '{type}' request -> Connected to: {addr}"
        else:
            return f"{status} for '{type}' request -> Connected to: {addr} -> Error: {error}"
        
    else:
        if error == "":
            return f"{status} for '{type}' request -> Connected to: {addr} -> File name: '{filename}'"
        else:
            return f"{status} for '{type}' request -> Connected to {addr} -> File name: '{filename}' -> Error: {error}"
       

def send_file(socket, filename, addr):
    """Read file with given filename and send data over network via provided socket"""

    try:
        # Read entire file in binary mode
        with open(filename,"rb") as file:
            data = file.read()

            # Sends data with delimiter on the end
            data += DELIMITER
            socket.sendall(data)

        return (True,"")

    except ConnectionResetError:
        return (False, "Connection broken so send failed.")

    except Exception as e:
        return (False, e)


def recv_file(socket, filename, addr):
    """Create file with given filename and write to it data received via provided socket"""

    try:
        file_contents = bytearray()

        # Receives file contents
        while True:
            data = socket.recv(1024)
            if data:
                file_contents += data
            if not data or len(data) < 1024:
                break
        
        # Checks that delimiter is on transfer
        if file_contents[-5:] != DELIMITER:
            raise Exception("File transfer incomplete.")

        # Writes file data in exlusive creation, binary mode
        with open(filename,"xb") as file:
            file.write(file_contents[:-5])

        return (True,"")

    except ConnectionResetError:
        return (False,"Connection broken so download failed.")

    except Exception as e:
        return (False, e)
    

def send_listing(socket, addr):
    """Generate and send directory listing from server to client via provided socket"""

    try:
        # Puts directory contents into a string
        dir_contents_list = os.listdir()
        dir_contents_str = "\n".join(dir_contents_list)

        # Sends with delimeter on the end
        socket.sendall(str.encode(dir_contents_str) + DELIMITER)
        
        return (True,"")
    
    except Exception as e:
        return (False,e)
    

def recv_listing(socket, addr):
    """Receive listing from server via provided socket and print it"""

    try:
        data = socket.recv(4096)

        # Checks that delimiter is on the transfer
        if data[-5:] != DELIMITER:
            raise Exception("Directory transfer incomplete.")

        # Prints directory contents
        directory_list = data[:-5].decode()
        print("\nContents of directory: ")
        print(directory_list)
        print()
        
        return (True, "")

    except Exception as e:
        return (False,e)
