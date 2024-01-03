# Introduction
For this project, we implemented several attacks and defenses. First, we discribe the attacks, then the defense and finally we explain how to launch all the attacks and defenses. 

# ATTACKS
We implemented different types of attacks : 
- brute force for credentials on the FTP server (`bruteforce.py`). The scripts needs a file containing passwords to do the bruteforce.
- Different types of (D)DOS (`ddos.py`)
    - Synflood : spam the destination with SYN requests.
    - pingflood : spam the destination with pings.
    - ping of death : spam the destination with pings that exceed the maximum size in order to overwhelm the network and to crash the system.
    - DRDoS with DNS serv : spam the destination with DNS response.
- Two types of network scanners (`network_scan.py`)
    - ARP scanner : scan the network using ARP request/response.
    - ICMP scanner : scan the network using ICMP echo/reply.
- ARP cache poisoning (`arpcache.py`) : Sends fake ARP replies in order for the attacker to forward traffic to its machine.


# PROTECTION

## Brute force
Main idea : limit the number of connection an IP can do.
We add the IPs in a set called denylist. If they try to do more than 1 connection
per minute, they are timed out for 5 minutes.     


## DOS 
Main idea : limit the traffic. 
- SynFlood : We limit the tcp traffic up to 10 packets per second to avoid Syn Flood attacks but still allow legitimate requests to flow. 
- PingFlood :  we limit the ICMP traffic to a maximum of 1 packet per second to avoid Ping Flood attacks.
- Ping of death : only accepts ping that do not exceed a size threshold and that are not fragmented.
- Reflected DNS attack : limit the rate of DNS queries from outside.  



## Network Scan 
Idea for ARP : Limit the ARP **request** rate.

Idea for ICMP : block or limit the ICMP request.
The ICMP are already limited for ping from the outside. But for the inside we add
a rule that block ICMP request for the workstation subnet and limit the ping to the 
DMZ.



## ARP cache poisoning 
Idea for defense : limit the number of ARP **replies** (not request as for the network scan).

# HOW TO USE THE SCRIPTS

**Important** : the command `iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP ` has to be used (in the machine from where the attack is launched) before launching the attack scripts to avoid the kernel from RSTing the connection we want to create.

To launch the script, launch first xterm for the specified machine than the script.

## ATTACK : Brute force
Launch the script using `python bruteforce.py`. The username(s) can be added line 9 and the password file name line 11. The default username is mininet. The script is not to make it simpler to launch. 
The attack is launched from the internet :
`xterm internet` then `python bruteforce.py`. 


## ATTACK : (D)DOS
To launch the scripts : 
- `python synflood.py`
- `python pingflood.py`
- `python pingofdeath.py`
- `python reflectivedns.py`

The scripts use threads to make the attack more effective.
All the scripts have a `target_ip` (and `target_port` for `synflood.py`) variable to specify the target. By default, all the values are the IP of the FTP server.

The attack is launched from the internet :
`xterm internet` then `python bruteforce.py`. 


## ATTACK : Network scan
To launch the scripts : 
- `python icmpscan.py`
- `python arpscan.py`

The scripts will analyze the network and print the active IP they found. By default, they scan the workstation subnet. 
The scripts are to be launched from a workstation : `xterm ws3` then launch the scripts above. 

## ATTACK : ARP cache poisoning
To launch the script : `python arpache.py`
The attack tries to transform the ws3 workstation into a man in the middle. It can also be done by adding another workstation. But we used the initial topology. The goal of the script is to spam both ws2 and the r1 router into thinking that ws3 is r1 (for ws2) and ws2 (for r1). 

Once the attack is done, ws3 becomes a man in the middle.


## DEFENSE : Basic network 
All the rules needed for the basic network defense are in `basic`. To launch it : `nft -f basic`.

To initialize the table and all the chains for all the rules below. In has to be launched in `r1`, `r2`, `s1` and `s2`.  
Command :  `nft -f init`

## DEFENSE : Brute force
To add the rules :  `nft -f bruteforce`. 
These rules are to be used in `r2` and `r1` to prevent any outside attacker and any compromised workstation from bruteforcing.

## DEFENSE : DOS
To add the rules : `nft -f dos`. The rules prevent from all types of DOS attack described above. The comments in the script show what every part is intended for. The script has to be used in `r2` to prevent any outside attacker from DOSing.

## DEFENSE : Network Scan

To add the rules : `nft -f network_scan`.
The rules are to be used in `r1` and `s1` to limit any potential scan in the workstation subnet.

## DEFENSE : ARP cache poisoning
To add the rules : `nft -f arpcachepoison`. The rules are to be used in `s1` and `s2`.

