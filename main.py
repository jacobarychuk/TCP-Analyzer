import sys
from utils import *
import socket


def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	connections = {}

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header
		endianness = get_endianness(global_header)

		connection_number = 1

		# Read packet headers until EOF is reached
		for packet_header in iter(lambda: f.read(16), b''):			

			incl_len = int.from_bytes(packet_header[8:12], byteorder=endianness) # Extract incl_len from packet header
			packet_data = f.read(incl_len) # Read packet data

			source_address = get_source_address(packet_data)
			destination_address = get_destination_address(packet_data)
			source_port = get_source_port(packet_data)
			destination_port = get_destination_port(packet_data)

			# Identify unique connections
			connection_key = (source_address, source_port, destination_address, destination_port)
			if connection_key not in connections:
				connections[connection_key] = connection_number
				connection_number += 1

	# Print all connections
	for connection_key, number in connections.items():
		print(f"Connection {number}:")
		print("Source address:", connection_key[0])
		print("Destination address:", connection_key[2])
		print("Source port:", connection_key[1])
		print("Destination port:", connection_key[3])


if __name__ == "__main__":
	main()
