import sys
import socket
import config


def get_endianness(global_header):
	"""Return the endianness of a CAP/PCAP file based on the magic number in its global header."""
	# Extract magic_number from global header
	magic_number = int.from_bytes(global_header[:4], byteorder='big')
	# Determine endianness
	if magic_number == 0xa1b2c3d4:
		return 'big'
	elif magic_number == 0xd4c3b2a1:
		return 'little'
	else:
		print("Unsupported file format", file=sys.stderr)
		sys.exit(1)


def get_source_address(packet_data):
	"""Extract and return the source IP address from the packet data."""
	return socket.inet_ntoa(packet_data[config.IPV4_HEADER_OFFSET+12:config.IPV4_HEADER_OFFSET+16])


def get_destination_address(packet_data):
	"""Extract and return the destination IP address from the packet data."""
	return socket.inet_ntoa(packet_data[config.IPV4_HEADER_OFFSET+16:config.IPV4_HEADER_OFFSET+20])


def get_source_port(packet_data):
	"""Extract and return the source port from the packet data."""
	ihl_bytes = (packet_data[config.IPV4_HEADER_OFFSET] & 0x0F) * 4
	tcp_header_offset = 14 + ihl_bytes
	return int.from_bytes(packet_data[tcp_header_offset:tcp_header_offset+2], byteorder='big')


def get_destination_port(packet_data):
	"""Extract and return the destination port from the packet data."""
	ihl_bytes = (packet_data[config.IPV4_HEADER_OFFSET] & 0x0F) * 4
	tcp_header_offset = 14 + ihl_bytes
	return int.from_bytes(packet_data[tcp_header_offset+2:tcp_header_offset+4], byteorder='big')

def get_flags(packet_data):
	"""Extract, interpret, and return the flags from the TCP header in the packet data."""
	ihl_bytes = (packet_data[config.IPV4_HEADER_OFFSET] & 0x0F) * 4
	tcp_header_offset = 14 + ihl_bytes
	flags = int.from_bytes(packet_data[tcp_header_offset+12:tcp_header_offset+14], byteorder='big') # Mask to get the lower 9 bits
	flag_names = ["FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR", "NS"]
	flag_status = {flag_names[i]: bool(flags & (1 << i)) for i in range(9)} # Map each flag name to its corresponding bit
	return flag_status
