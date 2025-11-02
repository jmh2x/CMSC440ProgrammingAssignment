# Name: Govan Henry
# Assignment: Programming Assignment: Simple PING Application
# Due Date: 11/2/2025
# Course: CMSC 440 - Data Communications and Networking

import socket
import sys
import time
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
    if len(sys.argv) != 3:
        print("ERR - arg 1" if len(sys.argv) < 2 else "ERR - arg 2")
        sys.exit()

    s_host = sys.argv[1]
    try:
        s_port = int(sys.argv[2])
    except ValueError:
        print("ERR - arg 2")
        sys.exit()

    #create UDP socket and set timeout to 1 second
    try:
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_socket.settimeout(1)
    except:
        print("ERR - socket creation failed")
        sys.exit()

    #fields for the ping packet
    hostname = socket.gethostname()
    version = 1
    class_name = "VCU-CMSC440-FALL-2025"
    user_name = "Henry, Govan"

    rtts = []  #round-trip times
    lost = 0   #lost packets

    #send 10 ping packets
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

        #print packet before sending
        PacketInfo("---------- Ping Packet Header ----------",
                    "--------- Ping Packet Payload ----------",
                      packet)

        try:
            #send packet to server and wait for reply
            c_socket.sendto(json.dumps(packet).encode(), (s_host, s_port))
            reply, _ = c_socket.recvfrom(2048)
            recv_time = time.time()
            reply_packet = json.loads(reply.decode())

            #print received reply
            PacketInfo("----------- Received Ping Reply Header -----------",
                        "----------- Received Ping Reply Payload -----------",
                          reply_packet)

            #calculate and print RTT
            rtt_sec = recv_time - reply_packet['Timestamp'] #RTT in seconds(receive time - reply packet timestamp)
            rtt_ms = rtt_sec * 1000 #milliseconds
            rtt_us = rtt_sec * 1_000_000 #microseconds
            print(f"RTT: {rtt_us:.2f} µs :: {rtt_ms:.2f} ms :: {rtt_sec:.6f} s") #print RTT in microseconds, milliseconds, seconds
            rtts.append(rtt_us) #store RTT in microseconds

        except socket.timeout:
            #handle timeout if no reply received
            print("----------- Ping Reply Timed Out -----------")
            lost += 1 #increment lost packet count

    #summary statistics
    if rtts:
        min_rtt = min(rtts) #minimum RTT
        max_rtt = max(rtts) #maximum RTT
        avg_rtt = sum(rtts) / len(rtts) #average RTT
    else:
        min_rtt = max_rtt = avg_rtt = 0 #no RTTs recorded

    loss_rate = (lost / 10) * 100 #packet loss rate percentage
    print(f"Summary: {min_rtt:.2f} :: {max_rtt:.2f} :: {avg_rtt:.2f} :: {loss_rate:.0f}%") #print summary statistics

if __name__ == "__main__":
    main()

