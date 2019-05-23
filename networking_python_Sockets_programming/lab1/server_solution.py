# Michal Wolas 117308883

from socket import *
import datetime

# create a socket
s = socket(AF_INET, SOCK_STREAM)

# get the domain name of the machine
myMachine = gethostname()
port = 10000


server_address = ('localhost', 10000)#(myMachine, port)

print('*** Server is starting up on %s port %s ***' % server_address)
# Bind the socket to the host and port

# set up the server based on the domain name
s.bind(server_address)

# Listen for one incoming connections to the server
s.listen(1)

while True:

    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    connection, client_address = s.accept() # accept a connection from the client
    # open a file using clients IP as the name / append if it already existed
    file = open("user_at_" + client_address[0] + ".txt", "a+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # write the time stamp into the file
    file.write("Connection made: " + str(time) + " from " + client_address[0] + " \n")

    try:
        print('connection from ' +  str(client_address))
        # Receive the data in small chunks and retransmit it

        while True:
            # decode() function returns string object
            data = connection.recv(16).decode()
            # if block is executed as data arrives / otherwise it waits to receive
            if data:
                file.write("'" + data + "' at " + str(datetime.datetime.now().strftime("%H:%M:%S")) + "\n")
                print('received "%s"' % data)
                print('sending data back to the client')
                # encode() function returns bytes object
                connection.sendall(data.encode())
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # send a response message back / telling the user the message was logged
                connection.sendall((" Message was logged into a file at " + str(time)).encode())
            else: # if the connection was closed, close the file then break out of the loop
                print('no more data from, file has been logged', client_address)
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write("Connection ended at "+ str(time) + "\n\n")
                file.close()
                break

    finally:
        # Clean up the connection
        connection.close()

# now close the socket
s.close()