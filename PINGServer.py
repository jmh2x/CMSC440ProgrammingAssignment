# Name: Govan Henry
# Assignment: Programming Assignment - Simple PING Application
# Due Date: [Insert Due Date]
# Course: CMSC 440

import socket
import sys
import random
import json

# Function to print packet header and payload in the required format
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
    if len(sys.argv) != 2:
        print("ERR - arg 1")
        sys.exit()

    try:
        port = int(sys.argv[1])
        if port <= 0 or port >= 65536:
            raise ValueError
    except ValueError:
        print("ERR - arg 1")
        sys.exit()

    # Create UDP socket and bind to port
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(("", port))
        serverSocket.settimeout(1)  # Allow periodic Ctrl-C check
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"PINGServer's socket is created using port number {port} with IP address {ip_address}")
    except:
        print(f"ERR - cannot create PINGServer socket using port number {port}")
        sys.exit()

    try:
        while True:
            try:
                # Receive packet from client
                message, clientAddress = serverSocket.recvfrom(2048)
            except socket.timeout:
                continue  # Check for Ctrl-C again

            try:
                packet = json.loads(message.decode())
            except:
                continue  # Skip malformed packets

            # Simulate 30% packet loss
            seq = packet.get("SequenceNo", "?")
            drop_chance = random.randint(1, 10)
            status = "DROPPED" if drop_chance <= 3 else "RECEIVED"
            print(f"{clientAddress[0]} :: {clientAddress[1]} :: Seq# {seq} :: {status}")

            if status == "DROPPED":
                continue

            # Print received packet
            PacketInfo("----------Received Ping Packet Header----------",
                        "---------Received Ping Packet Payload------------",
                          packet)

            # Construct reply packet with capitalized payload
            reply_payload = "\n".join([line.upper() for line in packet.get("Payload", "").splitlines()])
            reply_packet = {
                "Version": packet.get("Version"),
                "SequenceNo": packet.get("SequenceNo"),
                "Timestamp": packet.get("Timestamp"),
                "Size": len(reply_payload),
                "Payload": reply_payload
            }

            # Print reply packet
            PacketInfo("----------- Ping Reply Header -----------",
                        "----------- Ping Reply Payload -----------",
                          reply_packet)

            # Send reply to client
            serverSocket.sendto(json.dumps(reply_packet).encode(), clientAddress)

    except KeyboardInterrupt:
        # shutdown on Ctrl-C
        serverSocket.close()

if __name__ == "__main__":
    main()
