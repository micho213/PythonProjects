# Michal Wolas 117308883
from socket import *
# create a socket
s = socket(AF_INET, SOCK_DGRAM)

# get the domain name of this machine
name = gethostname()

#DNS lookup of the ip address based on the domain name
ip_address = gethostbyname(name)

port = 6789

# show the domain name and ip and port
print(name, " ", ip_address, " : ", port)

# address tuple
server_address = (ip_address, port)


print("\nMessage will be Sent to :   %s :  %s   Via UDP \n" % server_address)

# loop to send multiple messages
while True:
    # get some input to send
    m = input("\nWhat would you like to send: ")

    # send message to the server at the address

    try:
        # to break out of the loop and close socket
        if m == "STOP":
            m = m.encode()
            s.sendto(m,(server_address)) # inform the server
            break

        # encode the message - change to bytes
        m = m.encode()
        s.sendto(m,(server_address))

        # listen for the reply

        reply = s.recv(4096)

        # print the reply
        print( "\nUDP server response : ")
        print(reply.decode())

    # attempting to catch common errors
    except TypeError:
        print("The message needs to be in bytes/encoded")
    except OverflowError:
        print("The server port/ip is incorrect")
    except:
        print("something failed")


# close the socket
s.close()