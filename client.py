import threading
import time
import random
import sys
import webbrowser
import os

import socket

# get command line arguments
# parameter1 = sys.argv[1]
# parameter2 = sys.argv[2]
#
# rsHostname = parameter1
# rsListenPort = int(parameter2)

#FOR TESTING ONLY - REMOVE LATER!!!
rsListenPort = 43000

def client():

    # Read hostnames into an array, line-by-line from input file (PROJ2-HNS.txt)
    with open("PROJ2-HNS.txt", "r") as hostFile:
        array = []
        for line in hostFile:
            # Trim extra ending characters
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.strip('\t')
            # Make line upper-case
            line = line.upper()
            # Add to array
            array.append(line)

    # Close file
    hostFile.close()

    # Create and open RESOLVED.txt for writing output
    resolved = open("RESOLVED.txt", "w+")

    # FOR TESTING - PRINT ARRAY
    print(array)

    # For each hostname:
    for i in array:

        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[C]: Client socket created")
        except socket.error as err:
            print('socket open error: {} \n'.format(err))
            exit()

        # Define the port on which you want to connect to the server
        port = rsListenPort
        localhost_addr = socket.gethostbyname(socket.gethostname())

        # connect to the rs server
        server_binding = (localhost_addr, rsListenPort)
        cs.connect(server_binding)
        print("CONNECTED!")

        # Send query to the server.
        cs.sendall(i)

        # Receive data from the server
        data_from_rs_server = cs.recv(100)
        print("[C]: Data received from RS server: {}".format(data_from_rs_server.decode('utf-8')))

        # close the client socket
        cs.close()
        print("CLIENT SOCKET CLOSED!")


        # write to file
        resolved.write(data_from_rs_server + "\n")

    resolved.close()


    return

client()
