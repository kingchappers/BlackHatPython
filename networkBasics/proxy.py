import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))
    except Exception as e:
        print("[!!] Failed to listen on %s:%d" % local_host,local_port)
        print("[!!] Check for other listening sockets or correct permissions")
        print("See below for full error details")
        print(e)
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host,local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connection information
        print("[==>] Received incoming connection from %s:%d" % (addr[0],addr[1]))

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_port,receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    #connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    #receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        #send it to the response handler
        remote_buffer = response_handler(remote_buffer)

        # if there is data to send to the local client, send it
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)
    # now loop and read from local, send to remote, send to local and repeat
    while True:
        #read from the local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            #send it to the request handler
            local_buffer = request_handler(local_buffer)

            #send data to the remote host
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")

            #receive the response
            remote_buffer = receive_from(remote_host)

            if len(remote_buffer):
                print("[<==] Received %d bytes from remote" % len(remote_buffer))
                hexdump(remote_buffer)

                #send to the response handler
                remote_buffer = response_handler(remote_buffer)

                #send response to local socket
                client_socket.send(remote_buffer)

                print("[<==] Sent to localhost")

            #if there's no more data close the connection
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print("[*] No more data. Closing connections")

                break

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2
    
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = " ".join(map("{0:0>2X".format,src))
        text = "".join([chr(x) if 0x20 <= x < 0x7F else "." for x in s])
        result.append("%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return "\n".join(result)

def main():

    #not parsing command line arguments in this one
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    #setup local listening parameters
    local_host  = sys.argv[1]
    local_port  = int(sys.argv[2])

    #setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    #this tells the proxy to connect and receive data
    #before sending to the remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # spin up the listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

main()

