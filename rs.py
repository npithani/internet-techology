import sys
import threading
import time
import random

import socket

# get command line arguments
parameter0 = sys.argv[1]
parameter1 = int(parameter0)

# rsListenPort = 50008
rsListenPort = parameter1

def rootserver():

    # Get number of lines in the input file (to use for hashtable)
    i = -1
    with open('PROJI-DNSRS.txt') as x:
        for i, l in enumerate(x):
            pass
    fileLength = i+1

    # Create empty dictionary
    rsDict = {}

    # Read file line by line
    with open("PROJI-DNSRS.txt", "r") as myFile:

        for line in myFile:

            # Make line upper-case
            line = line.upper()

            # Trim newline characters
            line = line.strip('\n')

            # Check for flag A
            if " A" in line:

                # Divide string into substrings
                field1, field2, field3 = line.split()

                # Add values to RS dictionary
                rsDict[field1] = field2;

            # Get TSHostname
            else:
                # Divide string into substrings
                field1, field2, field3 = line.split()
                ts_hostname = field1

    # Close file
    myFile.close()

    print(rsDict)

    # Make a socket, bind port to rsListenPort, and put it in listen mode
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: RS Server socket created")
    except socket.error as err:
        print('RS socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', rsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[RS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[RS]: Server IP address is {}".format(localhost_ip))

    # Process client request
    while True:
        # Accept client connection
        csockid, addr = ss.accept()
        print ("[RS]: Got a connection request from a client at {}".format(addr))

        # Get upper-case hostname from client
        toQuery = csockid.recv(1024)
        toQuery = toQuery.upper()
        print(toQuery)

        # Look up hostname in DNS table
        if toQuery in rsDict:
            ipAddress = rsDict[toQuery]
            sendString = toQuery + " " + ipAddress + " A"
        else:
            # Get IP address of local machine
            hostname = socket.gethostname()
            IP = socket.gethostbyname(hostname)
            print("IP: " + IP)
            sendString = IP + " - NS"

        # Send client response
        csockid.send(sendString.encode('utf-8'))

    # Close socket connection
    ss.close()


    return


# Call functions to run them
rootserver()


