#!/usr/bin/env python3

import socket
import os

#host to listen on - set this to the current IP
host = "192.168.1.98"

#create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

#include the IP headers in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#If this is on Windows send an IOCTL to set up promiscuous mode
#IOCTL (input/output control) allows userspace programs to communicate with kernel mode components
if os.name == "nt":
    #pylint reports errors in this and the lower ioctl, this is okay and the code works
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

#read in a packet
print(sniffer.recvfrom(65565))

#if in Windows, turn off promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

#attempt to start an nmap scan on discovered hosts