# Michal Wolas 117308883
from socket import *
import datetime
# create a socket
s = socket(AF_INET, SOCK_DGRAM)

# get the domain name of this machine
name = gethostname()

#DNS lookup of the ip address based on the domain name
ip_address = gethostbyname(name)

port = 6789

print(name, " ", ip_address, " : ", port)

#address tuple
server_address = (ip_address, port)

# bind the socket to its address
print('Server running:   %s : %s  ' % server_address)

try:
    s.bind((ip_address,port))
except:
    print("address already binded, please try again / free the address")

# opens the log file
try:
    save_file = open("clientLog", "a+")
except:
    print("couldn't open file")

while True:
    print("\n ----- waiting for a Message (UDP) ------ \n")

    # wait for a message from the client
    # address is the address of the client as tuple
    data, address = s.recvfrom(4096)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # print the decoded message
    print(data.decode())

    # if the client closes its socket it will inform the server
    if data.decode() == "STOP":
        break

    reply = data.decode()

    print("Logging client message...")

    # write to the log file
    try:
        save_file.write("message from : " + str(address) + "\n")
        save_file.write("at: " + str(time) + "\n'")
        save_file.write(reply + "'\n\n")
    except:
        print("The file has been closed / is not responding")


    # change message to upper case
    reply = reply.upper()

    reply += " at: " + str(time)
    # encode/change to bytes
    reply = reply.encode()

    print("sending reply to the client...")

    # send the reply to the address that the message was received from
    try:
        s.sendto(reply,(address))
    except:
        print("couldn't send the reply, possibly wrong address")


# close the file and the socket
save_file.close()
s.close()