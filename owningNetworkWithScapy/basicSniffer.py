#!/usr/bin/env python3

from scapy.all import *

#packet callback
def packet_callback(packet):
    print(packet.show())

#start the sniffer
#filter - allows you to set Wireshark (BPF) style filters on packets to capture
#prn - specifies callback tfunction to be called for packets that match the filter
#store - sets number of packets stored in memory. We're keeping none. 
#count - sets the number of packets to capture. If not there default is indefinite
sniff(prn=packet_callback, count=1)