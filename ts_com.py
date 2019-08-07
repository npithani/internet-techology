import sys
import threading
import time
import random

import socket

# get command line arguments
# parameter0 = sys.argv[1]
# tsEduListenPort = int(parameter0)

# FOR TESTING ONLY - REMOVE LATER!!!!
tsComListenPort = 47000


def tcomserver():

    # Create empty dictionary
    tscDict = {}

    # Read file line by line
    with open("PROJ2-DNSTScom.txt", "r") as myFile:

        for line in myFile:

            # Make line upper-case
            line = line.upper()

            # Trim newline characters
            line = line.strip('\n')

            # Check for flag A
            if " A" in line:

                # Divide string into substrings
                field1, field2, field3 = line.split()

                # Add values to TS dictionary
                tscDict[field1] = field2;

            # Get TSHostname
            else:
                # Divide string into substrings
                field1, field2, field3 = line.split()
                ts_hostname = field1

    # Close file
    myFile.close()

    print(tscDict)

    # Make a socket, bind port to tsEduListenPort, and put it in listen mode
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS_COM]: TS Server socket created")
    except socket.error as err:
        print('TS_COM socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', tsComListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS_COM]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS_COM]: Server IP address is {}".format(localhost_ip))

    # Process RS request
    while True:
        # Accept RS connection
        csockid, addr = ss.accept()
        print ("[TS_COM]: Got a connection request from RS at {}".format(addr))

        # Get upper-case hostname from RS
        toQuery = csockid.recv(1024)
        toQuery = toQuery.upper()
        print(toQuery)

        # Look up hostname in DNS table
        if toQuery in tscDict:
            ipAddress = tscDict[toQuery]
            sendString = toQuery + " " + ipAddress + " A"
        else:
            sendString = toQuery + " - ERROR:HOST NOT FOUND"

        print(sendString)

        # Send RS response
        csockid.send(sendString.encode('utf-8'))

    # Close socket connection
    ss.close()


    return


# Call functions to run them
tcomserver()


