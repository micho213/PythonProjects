# Michal Wolas 117308883
from socket import *
import sys
from time import perf_counter
import statistics
import datetime

try:
    sysArguments = sys.argv
    times_to_ping = int(sysArguments[1])
    ip_address = sysArguments[2]
except:
    print("USAGE: 'python pingNumber IPAddress'")
    exit()

# create a socket
s = socket(AF_INET, SOCK_DGRAM)

port = 12000
# address tuple
server_address = (ip_address, port)

# settimeout sets how long the socket should wait for a response , if it times out it throws an error
s.settimeout(1)

fails = 0  # number of messages that didn't come back
RTT = []  # contains round trip times of packets that arrived

print("\nPING %s:%s VIA UDP " % server_address)

for i in range(times_to_ping):
    # making the message to send
    # ping sequence_number time
    pingMSG = "ping "
    pingMSG += str(i) + "  "
    pingMSG += str(datetime.datetime.now())

    # encode the message
    pingMSG = pingMSG.encode()

    # start the timer
    s1 = perf_counter()
    # send via UDP
    try:
        s.sendto(pingMSG, server_address)  # inform the server
    except:
        print("There was issues with the address, couldn't send ping to:  ", server_address)
    # try to receive, except it timed out
    try:

        reply = s.recv(4096)
        # stop timer
        s2 = perf_counter()
        # calculate the time taken and add it to the RTT
        time = (s2 - s1) * 1000
        RTT += [time]

        print("%d bytes from %s: UDP_seq=%d time=%.5f ms" % (len(reply), ip_address, i, time))

    # catches the socket timeout
    except:
        # the Packet was lost and request timed out
        print("Request timed out.")
        fails += 1

# close the socket
s.close()

# produce all the statistics
min = min(RTT)
max = max(RTT)
average = (sum(RTT) / len(RTT))
packet_loss = (fails / times_to_ping) * 100
# standard deviation
stddev = statistics.stdev(RTT)
print("\n--- %s ping statistics ---" % ip_address)
print("%d packets transmitted, %d packets received, %.2f %% packet loss"
      % (times_to_ping, (times_to_ping - fails), packet_loss))
print("round-trip min/avg/max/stddev = %.5f/%.5f/%.5f/%.5f ms" % (min, average, max, stddev))
