import socket
import sys
import time
import json

def print_packet(header_title, payload_title, packet):
    print(header_title)
    print(f"Version: {packet['Version']}")
    print(f"Sequence No.: {packet['SequenceNo']}")
    print(f"Time: {packet['Timestamp']}")
    print(f"Payload Size: {packet['Size']}")
    print(payload_title)
    for line in packet['Payload'].splitlines():
        print(line)

def main():
    if len(sys.argv) != 3:
        print("ERR - arg 1" if len(sys.argv) < 2 else "ERR - arg 2")
        sys.exit()

    server_host = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("ERR - arg 2")
        sys.exit()

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1)
    except:
        print("ERR - socket creation failed")
        sys.exit()

    hostname = socket.gethostname()
    version = 1
    class_name = "VCU-CMSC440-FALL-2024"
    user_name = "Henry, Govan"

    rtts = []
    lost = 0

    for seq in range(1, 11):
        timestamp = time.time()
        payload = f"Host: {hostname}\nClass-name: {class_name}\nUser-name: {user_name}"
        packet = {
            "Version": version,
            "SequenceNo": seq,
            "Timestamp": timestamp,
            "Size": len(payload),
            "Payload": payload
        }

        print("---------- Ping Packet Header")
        print(f"Version: {version}")
        print(f"Sequence No.: {seq}")
        print(f"Time: {timestamp}")
        print(f"Payload Size: {len(payload)}")
        print("--------- Ping Packet Payload ----------")
        for line in payload.splitlines():
            print(line)

        try:
            client_socket.sendto(json.dumps(packet).encode(), (server_host, server_port))
            reply, _ = client_socket.recvfrom(2048)
            recv_time = time.time()
            reply_packet = json.loads(reply.decode())

            print("----------- Received Ping Reply Header -----------")
            print(f"Version: {reply_packet['Version']}")
            print(f"Sequence No.: {reply_packet['SequenceNo']}")
            print(f"Time: {reply_packet['Timestamp']}")
            print(f"Payload Size: {reply_packet['Size']}")
            print("----------- Received Ping Reply Payload -----------")
            for line in reply_packet['Payload'].splitlines():
                print(line)

            rtt_sec = recv_time - reply_packet['Timestamp']
            rtt_ms = rtt_sec * 1000
            rtt_us = rtt_sec * 1_000_000
            print(f"RTT: {rtt_us:.2f} µs :: {rtt_ms:.2f} ms :: {rtt_sec:.6f} s")
            rtts.append(rtt_us)

        except socket.timeout:
            print("----------- Ping Reply Timed Out -----------")
            lost += 1

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
