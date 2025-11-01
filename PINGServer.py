# Name: Govan Henry
# Assignment: Programming Assignment - Simple PING Application
# Course: CMSC 440 - Fall 2024
# Due Date: [Insert Due Date]

import socket
import sys
import random

def parse_header_payload(data):
    lines = data.decode().splitlines()

    # Validate expected structure
    if len(lines) < 7:
        raise ValueError("Incomplete packet")

    # Skip divider line at index 0
    header = {
        "Version": lines[1].split(":")[1].strip(),
        "SequenceNo": int(lines[2].split(":")[1].strip()),
        "Timestamp": float(lines[3].split(":")[1].strip()),
        "Size": int(lines[4].split(":")[1].strip())
    }

    # Skip divider line at index 5
    payload = lines[6:]
    return header, payload

def capitalize_payload(payload_lines):
    return [line.upper() for line in payload_lines]

def format_reply(header, payload_lines):
    reply = []
    reply.append("----------- Ping Reply Header -----------")
    reply.append(f"Version: {header['Version']}")
    reply.append(f"Sequence No.: {header['SequenceNo']}")
    reply.append(f"Time: {header['Timestamp']}")
    reply.append(f"Payload Size: {header['Size']}")
    reply.append("----------- Ping Reply Payload -----------")
    reply.extend(payload_lines)
    return "\n".join(reply)

def main():
    if len(sys.argv) != 2:
        print("ERR - arg 1")
        sys.exit()

    try:
        port = int(sys.argv[1])
        if not (0 < port < 65536):
            raise ValueError
    except ValueError:
        print("ERR - arg 1")
        sys.exit()

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(("", port))
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"PINGServer's socket is created using port number {port} with IP address {ip_address}")
    except:
        print(f"ERR - cannot create PINGServer socket using port number {port}")
        sys.exit()

    while True:
        try:
            message, clientAddress = serverSocket.recvfrom(2048)
            try:
                header, payload = parse_header_payload(message)
            except Exception as e:
                print(f"Error: {e}")
                continue

            # Simulate packet loss
            drop_chance = random.randint(1, 10)
            seq = header["SequenceNo"]
            client_ip, client_port = clientAddress
            if drop_chance <= 3:
                print(f"{client_ip} :: {client_port} : {seq} :: DROPPED")
                continue
            else:
                print(f"{client_ip} :: {client_port} : {seq} :: RECEIVED")

            # Print received packet
            print("■ Received Ping Packet Header")
            print(f"Version: {header['Version']}")
            print(f"Sequence No.: {header['SequenceNo']}")
            print(f"Time: {header['Timestamp']}")
            print(f"Payload Size: {header['Size']}")
            print("■ Received Ping Packet Payload")
            for line in payload:
                print(line)

            # Capitalize payload and send back
            capitalized_payload = capitalize_payload(payload)
            reply = format_reply(header, capitalized_payload)
            serverSocket.sendto(reply.encode(), clientAddress)

        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()

