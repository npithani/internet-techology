import threading
import time
import random
import sys

import socket

# get command line arguments
parameter1 = sys.argv[1]
parameter2 = sys.argv[2]
parameter3 = sys.argv[3]

rsHostname = parameter1
rsListenPort = parameter2
tsListenPort = parameter3

def client():

    # Read hostnames into an array, line-by-line from input file (PROJI-HNS.txt)
    with open("PROJI-HNS.txt", "r") as hostFile:
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
        print("[C]: Data received from server: {}".format(data_from_rs_server.decode('utf-8')))

        # close the client socket
        cs.close()
        print("CLIENT SOCKET CLOSED!")

        # If the rs server doesn't have the IP address of the hostname
        if "NS" in data_from_rs_server:

            # Get TSHostname from response by removing flag value
            new_data = data_from_rs_server[:-5]
            print("ts ip address is : " + new_data)

            # Make socket with TS hostname and port number
            try:
                ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[C]: Second client socket created")
            except socket.error as err:
                print('socket open error: {} \n'.format(err))
                exit()

            # Define the port on which you want to connect to the server
            port = tsListenPort
            localhost_addr = socket.gethostbyname(socket.gethostname())

            # connect to the rs server
            server_binding = (new_data, port)
            ds.connect(server_binding)
            print("CONNECTED!")

            # Send query to the server.
            ds.sendall(i)

            # Receive data from the server
            data_from_ts_server = ds.recv(100)
            print("[C]: Data received from server: {}".format(data_from_ts_server.decode('utf-8')))

            # close the socket
            cs.close()

            # write to file
            resolved.write(data_from_ts_server + "\n")

        # If the RS response had the information needed
        else:

            # write to file
            resolved.write(data_from_rs_server + "\n")


    return

client()
