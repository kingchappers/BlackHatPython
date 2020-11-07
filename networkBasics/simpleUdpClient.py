import socket

target_host = "127.0.0.1"
target_port = 5005 

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(b'AAABBBCCC',(target_host,target_port))

# receive some data
data, addr = client.recvfrom(1024)

print(data)

# this code assumes 3 things

# 1 - The connection will always succeed
# 2 - The server is always expecting us to send data first
# 3 - The server will always send back data in a timely fashion