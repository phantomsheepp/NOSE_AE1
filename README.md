# NOSE_AE1

Things to do:

  * lots of error checking and management
  * fix janky way of sending files?
  * add summary print messages confirming actions that have taken place
  * add comments
  * add nice way to close server

Updated things to do:

  * file name error checking 
    * exists
    * has file extension
    * if contains any special characters - either works or stops you 
    * did you mean?

  * change receive to only receive at the start (so it includes the file contents)

  * more error exceptions





##############################
Had an idea for making a nice way to close the server which involved reading any user input but then it waits indefinitely until user inputted something...idk


user_input = sys.stdin.readline()
if user_input == "exit\n": # The user requested that the communication is terminated
    print("User-requested exit")
    break