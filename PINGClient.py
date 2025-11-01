# Name: Govan Henry
# Assignment: Programming Assignment - Simple PING Application
# Due Date: [Insert Due Date]
# Course: CMSC 440

import socket
import sys
import time
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
    if len(sys.argv) != 3:
        print("ERR - arg 1" if len(sys.argv) < 2 else "ERR - arg 2")
        sys.exit()

    server_host = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("ERR - arg 2")
        sys.exit()

    # Create UDP socket and set timeout to 1 second
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1)
    except:
        print("ERR - socket creation failed")
        sys.exit()

    # Prepare static and dynamic fields for the ping packet
    hostname = socket.gethostname()
    version_str = "1.0"
    version = int(version_str.split('.')[0])  # Version field as byte
    class_name = "VCU-CMSC440-FALL-2025"
    user_name = "Henry, Govan"

    rtts = []  # Store round-trip times
    lost = 0   # Count lost packets

    # Send 10 ping packets
    for seqno in range(1, 11):
        timestamp = time.time()
        payload = f"Host: {hostname}\nClass-name: {class_name}\nUser-name: {user_name}"
        packet = {
            "Version": version,
            "SequenceNo": seqno,
            "Timestamp": timestamp,
            "Size": len(payload),
            "Payload": payload
        }

        # Print packet before sending
        PacketInfo("---------- Ping Packet Header ----------",
                    "--------- Ping Packet Payload ----------",
                      packet)

        try:
            # Send packet and wait for reply
            client_socket.sendto(json.dumps(packet).encode(), (server_host, server_port))
            reply, _ = client_socket.recvfrom(2048)
            recv_time = time.time()
            reply_packet = json.loads(reply.decode())

            # Print received reply
            PacketInfo("----------- Received Ping Reply Header -----------",
                        "----------- Received Ping Reply Payload -----------",
                          reply_packet)

            # Calculate and print RTT
            rtt_sec = recv_time - reply_packet['Timestamp']
            rtt_ms = rtt_sec * 1000
            rtt_us = rtt_sec * 1_000_000
            print(f"RTT: {rtt_us:.2f} µs :: {rtt_ms:.2f} ms :: {rtt_sec:.6f} s")
            rtts.append(rtt_us)

        except socket.timeout:
            # Handle timeout if no reply received
            print("----------- Ping Reply Timed Out -----------")
            lost += 1

    # Print summary statistics
    if rtts:
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = sum(rtts) / len(rtts)
    else:
        min_rtt = max_rtt = avg_rtt = 0

    loss_rate = (lost / 10) * 100
    print(f"Summary: {min_rtt:.2f} :: {max_rtt:.2f} :: {avg_rtt:.2f} :: {loss_rate:.0f}%")

if __name__ == "__main__":
    main()
