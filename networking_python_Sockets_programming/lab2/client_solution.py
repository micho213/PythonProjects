# Michal Wolas 117308883
from socket import *

# create a socket
s = socket(AF_INET, SOCK_STREAM)

# get the domain name of this machine
name = gethostname()
print("Domain name = " + name)

# get the ip address based on the domain name
ip_address = gethostbyname(name)
print("ip address of the machine : " + ip_address)

port = 10000
print("at port: " + str(port))

server_address = (ip_address, port)

print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port

# connect to the server at the IP address and port number
s.connect(server_address)

user_message = ""
userNotFinished = False
# this loop will allow the user to send multiple messages per connection


def close():
    print("Closing the socket...")
    s.close()
    return False

while not userNotFinished:

    user_message = input("To send:  / or 'STOP': ")
    x = True

    try:
        if user_message == "STOP":
            user_message += "END"
            s.sendall(user_message.encode()) # send the message with END at the end.
            userNotFinished = True
            close()
            break

        msg = ""  # holds the response
        print("Sent")
        # send the message to the server
        s.sendall(user_message.encode())
        s.send("END".encode())  # prefix added to the end so the server recognises that the whole message has been sent

        print("waiting for a response...")
        while True:
            data = s.recv(64).decode()
            msg += str(data)
            if data[-3:] == "END":  # if end is in the last thing received
                break
            if data == "STOP": # STOP message sent by the server to inform the client that connection has been stopped
                print("Connection stopped")
                x = close()
                break

        if not x: # if server stopped the connection exit the loop
            break
        print('\n %s \n' % msg[:-3])
    except:
        print("Something failed")





