# Michal Wolas 117308883

from socket import *
import datetime

# create a socket
s = socket(AF_INET, SOCK_STREAM)

# get the domain name of the machine
myMachine = gethostname()
port = 10000

server_address = (myMachine, port)

print('*** Server is starting up on %s port %s ***' % server_address)
# Bind the socket to the host and port

# set up the server based on the domain name
s.bind(server_address)
# Listen for one incoming connections to the server
s.listen(1)


def close():  # closes the files and returns false so the loop and be exited
    print('no more data from, file has been logged', client_address)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write("Connection ended at " + str(time) + "\n\n")
    file.close()
    return False


while True:
    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    connection, client_address = s.accept()  # accept a connection from the client
    # open a file using clients IP as the name / append if it already existed
    file = open("user_at_" + client_address[0] + ".txt", "a+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # write the time stamp into the file
    file.write("Connection made: " + str(time) + " from " + client_address[0] + " \n")
    x = True
    try:
        print('connection from ' + str(client_address))
        # Receive the data in small chunks and retransmit it
        msg = ""
        while True:

            while True:
                data = connection.recv(64).decode()
                msg += str(data)

                if data[-3:] == "END":
                    if data == "STOPEND":
                        x = close()
                    break
            if not x:  # if the client stopped the conenction break out of the loop
                break

            if data:
                file.write("'" + msg[:-3] + "' at " + str(datetime.datetime.now().strftime("%H:%M:%S")) + "\n")
                print('\n %s \n' % msg[:-3])  # display the message received
                msg = ""  # clear it for next time
                response = input("To send:  / or 'STOP': ")
                # encode() function returns bytes object
                if response == "STOP":  # check if the server wants to terminate
                    connection.send(response.encode())  # inform the client that we are terminating
                    break

                print("sent")
                print("waiting for a response...")
                connection.sendall(response.encode())  # send the response to the client
                connection.send(
                    "END".encode())  # prefix added to the end so the client recognises that the whole message has been sent
                # log the response
                file.write(
                    "response: '" + response[:-3] + "' at " + str(datetime.datetime.now().strftime("%H:%M:%S")) + "\n")

            else:  # if the connection was closed, close the file then break out of the loop
                close()  # closes file
                break  # break out to close connection
    finally:
        # Clean up the connection
        connection.close()

# now close the socket
s.close()
