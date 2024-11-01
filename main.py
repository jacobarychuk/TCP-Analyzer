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
				direction = 'forward'
			elif (destination_address, destination_port, source_address, source_port) in connections:
				# Use the key where source and destination are swapped (preserve direction observed first)
				connection_key = (destination_address, destination_port, source_address, source_port)
				direction = 'reverse'
			else:
				# Store new bidirectional connections in the direction observed first
				connection_key = (source_address, source_port, destination_address, destination_port)
				connections[connection_key] = ConnectionInfo()
				direction = 'forward'

			connections[connection_key].add_packet(packet_header, packet_data, direction)

	# Print all connections
	print("Total number of connections:", len(connections))
	for n, (connection_key, connection_info) in enumerate(connections.items(), start=1):
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
			print("Number of packets sent from source to destination:", connection_info.get_packet_count_source_destination())
			print("Number of packets sent from destination to source:", connection_info.get_packet_count_destination_source())
			print("Total number of packets:", connection_info.get_packet_count())
			print("Number of data bytes sent from source to destination:", connection_info.get_byte_count_source_destination())
			print("Number of data bytes sent from destination to source:", connection_info.get_byte_count_destination_source())
			print("Total number of data bytes:", connection_info.get_byte_count())

	# Print summary of connection states
	complete_connections = [connection_info for connection_info in connections.values() if connection_info.get_end_time() is not None]
	reset_connections = [connection_info for connection_info in connections.values() if connection_info.reset]
	print("Number of complete connections:", len(complete_connections))
	print("Number of reset connections:", len(reset_connections))
	print("Number of connections still open when the trace capture ended:", len(connections) - len(complete_connections))

	# Print summary of complete connections
	if len(complete_connections) > 0:
		minimum_duration = min(connection_info.get_duration() for connection_info in complete_connections)
		average_duration = sum(connection_info.get_duration() for connection_info in complete_connections) / len(complete_connections) 
		maximum_duration = max(connection_info.get_duration() for connection_info in complete_connections)
		print(f"Minimum duration: {round(minimum_duration, 6)} seconds")
		print(f"Average duration: {round(average_duration, 6)} seconds")
		print(f"Maximum duration: {round(maximum_duration, 6)} seconds")
		minimum_packet_count = min(connection_info.get_packet_count() for connection_info in complete_connections)
		average_packet_count = sum(connection_info.get_packet_count() for connection_info in complete_connections) / len(complete_connections)
		maximum_packet_count = max(connection_info.get_packet_count() for connection_info in complete_connections)
		print("Minimum number of packets (sent/received):", minimum_packet_count)
		print("Average number of packets (sent/received):", round(average_packet_count, 6))
		print("Maximum number of packets (sent/received):", maximum_packet_count)


if __name__ == "__main__":
	main()
