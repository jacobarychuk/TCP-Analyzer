import sys
from utils import *
import socket
from connection_info import ConnectionInfo
import config


def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	connections = {}

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header
		config.endianness = get_endianness(global_header) # Set endianness

		# Read packet headers until EOF is reached
		for packet_header in iter(lambda: f.read(16), b''):			

			incl_len = int.from_bytes(packet_header[8:12], byteorder=config.endianness) # Extract incl_len from packet header
			packet_data = f.read(incl_len) # Read packet data

			source_address = get_source_address(packet_data)
			destination_address = get_destination_address(packet_data)
			source_port = get_source_port(packet_data)
			destination_port = get_destination_port(packet_data)

			# Identify unique bidirectional connections
			if (source_address, source_port, destination_address, destination_port) in connections:
				# Use the key as is
				connection_key = (source_address, source_port, destination_address, destination_port)
			elif (destination_address, destination_port, source_address, source_port) in connections:
				# Use the key where source and destination are swapped (preserve direction observed first)
				connection_key = (destination_address, destination_port, source_address, source_port)
			else:
				# Store new bidirectional connections in the direction observed first
				connection_key = (source_address, source_port, destination_address, destination_port)
				connections[connection_key] = ConnectionInfo()

			connections[connection_key].add_packet(packet_header, packet_data)

	# Print all connections
	print("Total number of connections:", len(connections))
	n = 1
	for connection_key, connection_info in connections.items():
		print(f"Connection {n}:")
		print("Source address:", connection_key[0])
		print("Destination address:", connection_key[2])
		print("Source port:", connection_key[1])
		print("Destination port:", connection_key[3])
		print("Status:", connection_info.get_status())
		if connection_info.get_end_time() is not None:
			print(f"Start time: {connection_info.get_start_time()} seconds")
			print(f"End time: {connection_info.get_end_time()} seconds")
			print(f"Duration: {connection_info.get_duration()} seconds")
		n += 1


if __name__ == "__main__":
	main()
