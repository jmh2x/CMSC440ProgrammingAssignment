import socket
import sys
import random
import json

def main():
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

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(("", port))
        serverSocket.settimeout(1)  # Allow periodic checks for Ctrl-C
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"PINGServer's socket is created using port number {port} with IP address {ip_address}")
    except:
        print(f"ERR - cannot create PINGServer socket using port number {port}")
        sys.exit()

    try:
        while True:
            try:
                message, clientAddress = serverSocket.recvfrom(2048)
            except socket.timeout:
                continue  # Check for Ctrl-C again

            try:
                packet = json.loads(message.decode())
            except:
                continue

            seq = packet.get("SequenceNo", "?")
            drop_chance = random.randint(1, 10)
            status = "DROPPED" if drop_chance <= 3 else "RECEIVED"
            print(f"{clientAddress[0]} :: {clientAddress[1]} :: Seq# {seq} :: {status}")

            if status == "DROPPED":
                continue

            print("Received Ping Packet Header")
            print(f"Version: {packet.get('Version')}")
            print(f"Sequence No.: {packet.get('SequenceNo')}")
            print(f"Time: {packet.get('Timestamp')}")
            print(f"Payload Size: {packet.get('Size')}")
            print("Received Ping Packet Payload")
            for line in packet.get("Payload", "").splitlines():
                print(line)

            reply_payload = "\n".join([line.upper() for line in packet.get("Payload", "").splitlines()])
            reply_packet = {
                "Version": packet.get("Version"),
                "SequenceNo": packet.get("SequenceNo"),
                "Timestamp": packet.get("Timestamp"),
                "Size": len(reply_payload),
                "Payload": reply_payload
            }

            print("----------- Ping Reply Header -----------")
            print(f"Version: {reply_packet['Version']}")
            print(f"Sequence No.: {reply_packet['SequenceNo']}")
            print(f"Time: {reply_packet['Timestamp']}")
            print(f"Payload Size: {reply_packet['Size']}")
            print("----------- Ping Reply Payload -----------")
            for line in reply_payload.splitlines():
                print(line)

            serverSocket.sendto(json.dumps(reply_packet).encode(), clientAddress)

    except KeyboardInterrupt:
        print("\nServer shutting down.")
        serverSocket.close()

if __name__ == "__main__":
    main()
