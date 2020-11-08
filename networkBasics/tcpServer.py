import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

# setting maximum backlog of connections to 5
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# this is the client handling thread and performs the recv and sends a message back to the client
def handle_client(client_socket):
    # print out whet the client sends
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send(b"ACK!")

    client_socket.close()

while True:
    # receive client socket into client variable and remote connection details into addr variable
    client,addr = server.accept()

    print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))

    # spin up the client thread to handle incoming data and pass it the client object
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()