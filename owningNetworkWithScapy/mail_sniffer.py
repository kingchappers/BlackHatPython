#!/usr/bin/env python3

from scapy.all import *

#packet callback
def packet_callback(packet):
    print(packet.show())

#start the sniffer
#can add a filter="" to the sniff which allows you to set a Wireshark (BPF) style filters on packets to capture
#prn - specifies callback tfunction to be called for packets that match the filter
sniff(prn=packet_callback,count=1)