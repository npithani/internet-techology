import sys
import threading
import time
import random

import socket

# get command line arguments
# parameter0 = sys.argv[1]
# parameter01 = sys.argv[2]
# parameter02 = sys.argv[3]
#
# # convert command line arguments to strings
# rsListenPort = int(parameter0)
# tsEduListenPort = int(parameter01)
# tsComListenPort = int(parameter02)

# FOR TESTING ONLY - REMOVE LATER!!!
rsListenPort = 43000
tsEduListenPort = 45000
tsComListenPort = 47000


def rootserver():

    # Create empty dictionary
    rsDict = {}

    # Read file line by line
    with open("PROJ2-DNSRS.txt", "r") as myFile:

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

            # Send client response
            csockid.send(sendString.encode('utf-8'))
        else:
            # Get IP address of local machine
            # hostname = socket.gethostname()
            # IP = socket.gethostbyname(hostname)
            # print("IP: " + IP)
            # sendString = IP + " - NS"

            # We need to check if the hostname ends in '.edu', '.com', or neither
            # Part One : if the hostname ends in '.edu'
            print("toQuery: " + toQuery)
            if '.EDU' in toQuery:

                print("present!")

                # Make socket with TS_edu hostname and port number
                try:
                    ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("[RS]: TS_edu socket created")
                except socket.error as err:
                    print('socket open error: {} \n'.format(err))
                    exit()

                # Define the port on which you want to connect to the server
                port = tsEduListenPort
                localhost_addr = socket.gethostbyname(socket.gethostname())

                # connect to the ts_edu server
                server_binding = (localhost_addr, port)
                ds.connect(server_binding)
                print("CONNECTED!")

                # Send query to the server.
                ds.sendall(toQuery)

                # Receive data from the server
                data_from_ts_edu_server = ds.recv(100)
                print("[RS]: Data received from server: {}".format(data_from_ts_edu_server.decode('utf-8')))

                # close the socket
                ds.close()

                # Send client response
                csockid.send(data_from_ts_edu_server.encode('utf-8'))

            # Part Two : if the hostname ends in '.com'
            elif '.COM' in toQuery:

                # Make socket with TS_edu hostname and port number
                try:
                    ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("[RS]: TS_com socket created")
                except socket.error as err:
                    print('socket open error: {} \n'.format(err))
                    exit()

                # Define the port on which you want to connect to the server
                port = tsComListenPort
                localhost_addr = socket.gethostbyname(socket.gethostname())

                # connect to the ts_edu server
                server_binding = (localhost_addr, port)
                ps.connect(server_binding)
                print("CONNECTED!")

                # Send query to the server.
                ps.sendall(toQuery)

                # Receive data from the server
                data_from_ts_com_server = ps.recv(100)
                print("[RS]: Data received from server: {}".format(data_from_ts_com_server.decode('utf-8')))

                # close the socket
                ps.close()

                # Send client response
                csockid.send(data_from_ts_com_server.encode('utf-8'))

            # hostname does not end in '.com' or '.edu', so send error message
            else:
                sendString = toQuery + " - ERROR:HOST NOT FOUND"

            # Send client response
            csockid.send(sendString.encode('utf-8'))


    # Close socket connection
    ss.close()


    return


# Call functions to run them
rootserver()