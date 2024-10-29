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

			ihl_bytes = (packet_data[ipv4_header_offset] & 0x0F) * 4 # Extract the length of IPv4 header from packet data and convert to bytes
			tcp_header_offset = 14 + ihl_bytes
			source_port = int.from_bytes(packet_data[tcp_header_offset:tcp_header_offset+2], byteorder='big') # Extract source port from packet data
			destination_port = int.from_bytes(packet_data[tcp_header_offset+2:tcp_header_offset+4], byteorder='big') # Extract destination port from packet data
			print("Source Port:", source_port)
			print("Destination Port:", destination_port)

			packet_number += 1


if __name__ == "__main__":
	main()
