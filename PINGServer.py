# Name: Govan Henry
# Assignment: Programming Assignment - Simple PING Application
# Due Date: [Insert Due Date]
# Course: CMSC 440

import socket
import sys
import random
import json

# Function to print packet header and payload
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
    # Validate command-line arguments
    if len(sys.argv) != 2: # if length of args is not 2
        print("ERR - arg 1") # print error for arg 1
        sys.exit()

    try:
        port = int(sys.argv[1]) # port number from arg 1
        if port <= 0 or port >= 65536: # port range(1-65535)
            raise ValueError # invalid port
    except ValueError: # invalid port
        print("ERR - arg 1") # print error for arg 1
        sys.exit()

    # Create UDP socket and bind to port
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create UDP socket
        serverSocket.bind(("", port)) # bind socket to port
        serverSocket.settimeout(1)  # timeout for server to check for ctrl c
        ip_address = socket.gethostbyname(socket.gethostname()) #ip address of socket
        print(f"PINGServer's socket is created using port number {port} with IP address {ip_address}")
    except:
        print(f"ERR - cannot create PINGServer socket using port number {port}")
        sys.exit()

    try:
        while True: # main server loop
            try: 
                # Receive packet from client
                message, clientAddress = serverSocket.recvfrom(2048)
            except socket.timeout: # timout for ctrl c check 
                continue  

            try:
                packet = json.loads(message.decode()) # parse received packet
            except:
                continue  # Skip malformed packets

            # Simulate 30% packet loss
            seq = packet.get("SequenceNo", "?") # get sequence number of packet
            drop_chance = random.randint(1, 10) # random number between 1-10 for drop chance
            status = "DROPPED" if drop_chance <= 3 else "RECEIVED" # 30% chance to drop packet
            print(f"{clientAddress[0]} :: {clientAddress[1]} :: Seq# {seq} :: {status}") # print seqiuence number and status

            if status == "DROPPED":
                continue

            #Print received packet from client
            PacketInfo("----------Received Ping Packet Header----------",
                        "---------Received Ping Packet Payload------------",
                          packet)

            # reply payload with uppercase letters
            reply_payload = "\n".join([line.upper() for line in packet.get("Payload", "").splitlines()])
            reply_packet = {
                "Version": packet.get("Version"),
                "SequenceNo": packet.get("SequenceNo"),
                "Timestamp": packet.get("Timestamp"),
                "Size": len(reply_payload),
                "Payload": reply_payload
            }

            # Print reply to client
            PacketInfo("----------- Ping Reply Header -----------" ,
                        "----------- Ping Reply Payload -----------",
                          reply_packet)

            # Send reply to client
            serverSocket.sendto(json.dumps(reply_packet).encode(), clientAddress)

    except KeyboardInterrupt:
        # shutdown on Ctrl-C
        serverSocket.close()

if __name__ == "__main__":
    main()
