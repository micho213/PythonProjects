# Michal Wolas 117308883

from socket import *

import sys

try:
    argList = sys.argv
    host = argList[1]
    port = argList[2]
    filename = argList[3]
except: # if incorrect arguments are provided
    print("Usage: client.py server_host server_port filename")
    exit()


# GET /HelloWorld.html HTTP/1.1

#create a socket
s = socket(AF_INET, SOCK_STREAM)

server_address = (host, int(port))

print('connecting to server at %s port %s' % server_address)

#connect to the server

s.connect(server_address)
request = "GET /" + filename + " HTTP/1.1"
try:
    print('sending...')
    # send the reques
    s.sendall(request.encode())
    response = ""
    data = True
    while data: # wait for the response
        data = s.recv(1024).decode()
        response += data

    print(response)
except:
    print("Something failed")


print("Closing the socket...")
s.close()
