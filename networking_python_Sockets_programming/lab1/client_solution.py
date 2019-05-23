# Michal Wolas 117308883
from socket import *

#create a socket
s = socket(AF_INET, SOCK_STREAM)

# get the domain name of this machine
name = gethostname()
print("Domain name = " + name)

# get the ip address based on the domain name
ip_address = gethostbyname(name)
print("ip address of the machine : " + ip_address)

port = 10000
print("at port: "+ str(port))

server_address = ('localhost', 10000)#(ip_address,port)

print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port

# connect to the server at the IP address and port number
s.connect(server_address)

user_message = ""
userNotFinished = False
# this loop will allow the user to send multiple messages per connection
while not userNotFinished:
    user_message += input("what message would you like to send / 'STOP': ")
    try:
        if user_message == "STOP":
            userNotFinished = True
            break
        print('sending...')
        # send the message to the server
        s.sendall(user_message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(user_message)
        timestamp = ""
        # while there is still data to receive
        while amount_received < amount_expected:
            data = s.recv(16).decode()
            amount_received += len(data)
            timestamp = s.recv(54).decode() # response message is exactly 54 characters long, so it receives 54 exactly

        print("success: " + timestamp)
        user_message = ""
    except:
        print("Something failed")
        user_message = ""


print("Closing the socket...")
s.close()




