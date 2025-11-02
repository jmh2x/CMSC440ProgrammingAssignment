# Name: Govan Henry
# Assignment: Programming Assignment: Simple PING Application
# Due Date: 11/2/2025
# Course: CMSC 440 - Data Communications and Networking

import socket
import sys
import random
import json

#function to print packet header and payload
def PacketInfo(header, payload, packet):
    print(header)
    print(f"Version: {packet['Version']}")
    print(f"Sequence No.: {packet['SequenceNo']}")
    print(f"Time: {packet['Timestamp']}")
    print(f"Payload Size: {packet['Size']}")
    print(payload)
    for line in packet['Payload'].splitlines():
        print(line)

def main():
    #validate command-line arguments
    if len(sys.argv) != 2: #if length of args is not 2
        print("ERR - arg 1") #print error for arg 1
        sys.exit()

    try:
        portno = int(sys.argv[1]) #port number from arg 1
        if portno <= 0 or portno >= 65536: #port range(1-65535)
            raise ValueError #invalid port
    except ValueError: 
        print("ERR - arg 1") #print error for arg 1
        sys.exit()

    #create UDP socket and bind to port
    try:
        sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create UDP socket
        sSocket.bind(("", portno)) #bind socket to port
        sSocket.settimeout(1)  #timeout for server to check for ctrl c
        ip_addr = socket.gethostbyname(socket.gethostname()) #ip address of socket
        print(f"PINGServer's socket is created using port number {portno} with IP address {ip_addr}")
    except:
        print(f"ERR - cannot create PINGServer socket using port number {portno}")
        sys.exit()

    try:
        while True: #main server loop
            try: 
                #receive packet from client
                message, clientAddress = sSocket.recvfrom(2048)
            except socket.timeout: #timout for ctrl c check 
                continue  

            try:
                packet = json.loads(message.decode()) #parse received packet
            except:
                continue #skip malformed packets

            #30% packet loss
            seqno = packet.get("SequenceNo", "?") #get sequence number of packet
            drop_chance = random.randint(1, 10) #random number between 1-10 for drop chance
            status = "DROPPED" if drop_chance <= 3 else "RECEIVED" #30% chance to drop packet
            print(f"{clientAddress[0]} :: {clientAddress[1]} :: Seq# {seqno} :: {status}") #print seqiuence number and status

            if status == "DROPPED":
                continue

            #print received packet from client
            PacketInfo("----------Received Ping Packet Header----------",
                        "---------Received Ping Packet Payload------------",
                          packet)

            #reply payload with uppercase letters
            reply_payload = "\n".join([line.upper() for line in packet.get("Payload", "").splitlines()])
            reply_packet = {
                "Version": packet.get("Version"),
                "SequenceNo": packet.get("SequenceNo"),
                "Timestamp": packet.get("Timestamp"),
                "Size": len(reply_payload),
                "Payload": reply_payload
            }

            #print reply to client
            PacketInfo("----------- Ping Reply Header -----------" ,
                        "----------- Ping Reply Payload -----------",
                          reply_packet)

            #send reply to client
            sSocket.sendto(json.dumps(reply_packet).encode(), clientAddress)

    except KeyboardInterrupt:
        #shutdown on Ctrl-C
        sSocket.close()

if __name__ == "__main__":
    main()
