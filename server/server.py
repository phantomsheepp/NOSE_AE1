import socket
import sys
from assessed_exercise import socket_to_screen, keyboard_to_socket

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" 
 Enclose the following two lines in a try-except block to catch
 exceptions related to already bound ports, invalid/missing
 command-line arguments, port number out of range, etc. Ideally,
 these errors should have been handled separately.
"""
try:
	"""
	 Register the socket with the OS kernel so that messages sent
	 to the user-defined port number are delivered to this program.
	 Using "0.0.0.0" as the IP address so as to bind to all available
	 network interfaces. Alternatively, could have used "127.0.0.1"
	 to bind only to the local (loopback) interface, or any other IP
	 address on an interface of the computer where this program is
	 running (use "ipconfig /all" to list all interfaces and their IP
	 addresses).
	"""
	srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
	
	"""
	 Create a queue where new connection requests will be added by
	 the OS kernel. This number should be small enough to not waste
	 resources at the OS level, but also large enough so that the
	 connections queue doesn't fill up. For this latter, one should
	 ideally have an idea of how long it takes to serve a request
	 and how frequently clients initiate new connections to the
	 server.
	"""
	srv_sock.listen(5)
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

# Loop forever (or at least for as long as no fatal errors occur)
while True:
	"""
	 Surround the following code in a try-except block to account for
	 socket errors as well as errors related to user input. Ideally
	 these error conditions should be handled separately.
	"""
	try:
		print("Waiting for new client... ")
		
		"""
		 Dequeue a connection request from the queue created by listen() earlier.
		 If no such request is in the queue yet, this will block until one comes
		 in. Returns a new socket to use to communicate with the connected client
		 plus the client-side socket's address (IP and port number).
		"""
		cli_sock, cli_addr = srv_sock.accept()
		cli_addr_str = str(cli_addr) # Translate the client address to a string (to be used shortly)

		print("Client " + cli_addr_str + " connected. Now chatting...")

		# Loop until either the client closes the connection or the user requests termination
		while True:
			# First, read data from client and print on screen
			bytes_read = socket_to_screen(cli_sock, cli_addr_str)
			if bytes_read == 0:
				print("Client closed connection.")
				break

			# Then, read data from user and send to client
			bytes_sent = keyboard_to_socket(cli_sock)
			if bytes_sent == 0:
				print("User-requested exit.")
				break

	finally:
		"""
		 If an error occurs or the client closes the connection, call close() on the
		 connected socket to release the resources allocated to it by the OS.
		"""
		cli_sock.close()

# Close the server socket as well to release its resources back to the OS
srv_sock.close()

# Exit with a zero value, to indicate success
exit(0)
