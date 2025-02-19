# TCP Analyzer

## Dependencies
None. This project is built purely with the Python standard library.

## How It Works
The program processes a trace file and summarizes each TCP connection, identified by the following 4-tuple:
- IP address of the source node
- Port number of the source node
- IP address of the destination node
- Port number of the destination node

A comprehensive summary of all TCP connections is generated based on the processed data.

## Example
To test the program, you can use the sample capture file [`http.cap`](http.cap).

```
python main.py http.cap
```

Running this command produces the following output:

```
Total number of connections: 3

Connection 1:
Source address: 145.254.160.237
Destination address: 65.208.228.223
Source port: 3372
Destination port: 80
Status: S2F2
Start time: 0.0 seconds
End time: 30.063228 seconds
Duration: 30.063228 seconds
Number of packets sent from source to destination: 16
Number of packets sent from destination to source: 18
Total number of packets: 34
Number of data bytes sent from source to destination: 479
Number of data bytes sent from destination to source: 18364
Total number of data bytes: 18843

Connection 2:
Source address: 145.254.160.237
Destination address: 145.253.2.203
Source port: 3009
Destination port: 53
Status: S0F2
Start time: 2.553672 seconds
End time: 2.91419 seconds
Duration: 0.360518 seconds
Number of packets sent from source to destination: 1
Number of packets sent from destination to source: 1
Total number of packets: 2
Number of data bytes sent from source to destination: 55
Number of data bytes sent from destination to source: 154
Total number of data bytes: 209

Connection 3:
Source address: 145.254.160.237
Destination address: 216.239.59.99
Source port: 3371
Destination port: 80
Status: S0F0

Number of complete connections: 2
Number of reset connections: 0
Number of connections still open when the trace capture ended: 1

Minimum duration: 0.360518 seconds
Average duration: 15.211873 seconds
Maximum duration: 30.063228 seconds

Minimum number of packets (sent/received): 2
Average number of packets (sent/received): 18.0
Maximum number of packets (sent/received): 34

Minimum window size: 0 bytes
Average window size: 7432.666667 bytes
Maximum window size: 9660 bytes
```

The status field indicates the number of SYN (S) and FIN (F) segments seen in the connection.
