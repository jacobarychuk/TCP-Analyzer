import sys
import utils
import socket


def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header
		endianness = utils.get_endianness(global_header)

		packet_number = 1

		# Read packet headers until EOF is reached
		for packet_header in iter(lambda: f.read(16), b''):			

			incl_len = int.from_bytes(packet_header[8:12], byteorder=endianness) # Extract incl_len from packet header
			packet_data = f.read(incl_len) # Read packet data

			ipv4_header_offset = 14
			source_address = socket.inet_ntoa(packet_data[ipv4_header_offset+12:ipv4_header_offset+16]) # Extract source address from packet data
			destination_address = socket.inet_ntoa(packet_data[ipv4_header_offset+16:ipv4_header_offset+20]) # Extract destination address from packet data
			print(f"Packet {packet_number}:")
			print("Source Address:", source_address)
			print("Destination Address:", destination_address)

			packet_number += 1


if __name__ == "__main__":
	main()
