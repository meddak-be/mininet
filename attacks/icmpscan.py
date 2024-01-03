import scapy.all as scapy
import ipaddress

network = '10.1.0.0/24'

def icmpscan():
    live_hosts = []
    
    try:
        ip_network = ipaddress.ip_network(network)
        ip_list = [str(ip) for ip in ip_network]
        for ip_addr in ip_list:
            icmp_packet = scapy.IP(dst=ip_addr)/scapy.ICMP()

            # Send the packet and wait for responses
            ans, _ = scapy.sr(icmp_packet, timeout=3, verbose=False)
            # Process responses
            for response in ans:
                if response[1].haslayer(scapy.ICMP):
                    ip = response[1][scapy.IP].src
                    print(ip_addr, " is awake")
    except KeyboardInterrupt:
        exit(0)


icmpscan()