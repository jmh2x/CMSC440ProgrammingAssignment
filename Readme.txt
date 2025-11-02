Govan Henry  V#: V01070863
Assignment: Programming Assignment: Simple PING Application
Due Date: 11/2/2025
Course: CMSC 440 - Data Communications and Networking

# How to Compile and Run the Program:

1. Make sure Python 3.x is installed on your system.

2. Open one terminal and start the server with:
   python PINGServer.py 10500
   - You can use any port number between 1 and 65535.

3. Open another terminal and run the client with:
   python PINGClient.py localhost 10500
   - You can use either 'localhost' or the server's IP address.
   - The port number must match the one used by the server.

4. The server will continue running until manually stopped using Ctrl+C.
