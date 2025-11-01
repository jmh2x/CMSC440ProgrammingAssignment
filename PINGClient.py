import socket
import sys
import time
import platform
import statistics

def build_ping_packet(seq_num, hostname, first_name, last_name):
    version = 1
    timestamp = time.time()
    payload_lines = [
        f"Host: {hostname}",
        "Class-name: VCU-CMSC440-FALL-2024",
        f"User-name: {last_name}, {first_name}"
    ]
    payload = "\n".join(payload_lines)
    size = len(payload.encode())

    header = [
        "---------- Ping Packet Header ----------",
        f"Version: {version}",
        f"Sequence No.: {seq_num}",
        f"Time: {timestamp}",
        f"Payload Size: {size}",
        "---------- Ping Packet Payload ----------"
    ]
    packet = "\n".join(header + payload_lines)
    return packet, timestamp

def parse_reply(reply):
    lines = reply.decode().splitlines()
    header = {
        "Version": lines[1].split(":")[1].strip(),
        "SequenceNo": int(lines[2].split(":")[1].strip()),
        "Timestamp": float(lines[3].split(":")[1].strip()),
        "Size": int(lines[4].split(":")[1].strip())
    }
    payload = lines[6:]
    return header, payload

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

    first_name = "Govan"
    last_name = "Henry"  
    hostname = platform.node()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    rtts = []
    lost_packets = 0

    for seq in range(1, 11):
        packet, timestamp = build_ping_packet(seq, hostname, first_name, last_name)
        print(packet)
        try:
            client_socket.sendto(packet.encode(), (server_host, server_port))
            start = time.time()
            reply, _ = client_socket.recvfrom(2048)
            end = time.time()

            header, payload = parse_reply(reply)
            rtt_sec = end - header["Timestamp"]
            rtt_ms = rtt_sec * 1000
            rtt_us = rtt_sec * 1_000_000
            rtts.append(rtt_us)

            print("----------- Received Ping Reply Header -----------")
            print(f"Version: {header['Version']}")
            print(f"Sequence No.: {header['SequenceNo']}")
            print(f"Time: {header['Timestamp']}")
            print(f"Payload Size: {header['Size']}")
            print("----------- Received Ping Reply Payload -----------")
            for line in payload:
                print(line)
            print(f"RTT: {rtt_us:.2f} μs :: {rtt_ms:.2f} ms :: {rtt_sec:.6f} s\n")

        except socket.timeout:
            lost_packets += 1
            print("----------- Ping Reply Timed Out -----------\n")

    if rtts:
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = statistics.mean(rtts)
    else:
        min_rtt = max_rtt = avg_rtt = 0

    loss_rate = (lost_packets / 10) * 100
    print(f"Summary: {min_rtt:.2f} :: {max_rtt:.2f} :: {avg_rtt:.2f} :: {loss_rate:.0f}%")

if __name__ == "__main__":
    main()
