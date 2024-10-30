import sys
from utils import *
import socket


def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header
		endianness = get_endianness(global_header)

		packet_number = 1

		# Read packet headers until EOF is reached
		for packet_header in iter(lambda: f.read(16), b''):			

			incl_len = int.from_bytes(packet_header[8:12], byteorder=endianness) # Extract incl_len from packet header
			packet_data = f.read(incl_len) # Read packet data

			source_address = get_source_address(packet_data)
			destination_address = get_destination_address(packet_data)
			print(f"Packet {packet_number}:")
			print("Source Address:", source_address)
			print("Destination Address:", destination_address)

			source_port = get_source_port(packet_data)
			destination_port = get_destination_port(packet_data)
			print("Source Port:", source_port)
			print("Destination Port:", destination_port)

			packet_number += 1


if __name__ == "__main__":
	main()
