import scapy.all as scapy

network = '10.1.0.0/24'

def arpscan():
    request = scapy.ARP()
    request.pdst = network

    broadcast = scapy.Ether()
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'
    
    request_broadcast = broadcast / request
    clients = scapy.srp(request_broadcast, timeout = 1)[0]

    for element in clients:
        print(element[1].psrc , " is awake")

arpscan()