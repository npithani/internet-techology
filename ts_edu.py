import sys
import threading
import time
import random

import socket

# get command line arguments
# parameter0 = sys.argv[1]
# tsEduListenPort = int(parameter0)

# FOR TESTING ONLY - REMOVE LATER!!!!
tsEduListenPort = 45000


def teduserver():

    # Create empty dictionary
    tsDict = {}

    # Read file line by line
    with open("PROJ2-DNSTSedu.txt", "r") as myFile:

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
                tsDict[field1] = field2;

            # Get TSHostname
            else:
                # Divide string into substrings
                field1, field2, field3 = line.split()
                ts_hostname = field1

    # Close file
    myFile.close()

    print(tsDict)

    # Make a socket, bind port to tsEduListenPort, and put it in listen mode
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS_EDU]: TS Server socket created")
    except socket.error as err:
        print('TS_EDU socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', tsEduListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS_EDU]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS_EDU]: Server IP address is {}".format(localhost_ip))

    # Process RS request
    while True:
        # Accept RS connection
        csockid, addr = ss.accept()
        print ("[TS_EDU]: Got a connection request from RS at {}".format(addr))

        # Get upper-case hostname from RS
        toQuery = csockid.recv(1024)
        toQuery = toQuery.upper()
        print(toQuery)

        # Look up hostname in DNS table
        if toQuery in tsDict:
            ipAddress = tsDict[toQuery]
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
teduserver()


