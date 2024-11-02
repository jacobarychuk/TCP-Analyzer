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

def get_tcp_header_offset(packet_data):
	"Calculate and return the offset of the TCP header."
	ip_header_length_bytes = (packet_data[config.IPV4_HEADER_OFFSET] & 0x0F) * 4
	return ip_header_length_bytes + 14

def get_source_port(packet_data):
	"""Extract and return the source port from the packet data."""
	tcp_header_offset = get_tcp_header_offset(packet_data)
	return int.from_bytes(packet_data[tcp_header_offset:tcp_header_offset+2], byteorder='big')

def get_destination_port(packet_data):
	"""Extract and return the destination port from the packet data."""
	tcp_header_offset = get_tcp_header_offset(packet_data)
	return int.from_bytes(packet_data[tcp_header_offset+2:tcp_header_offset+4], byteorder='big')

def get_flags(packet_data):
	"""Extract, interpret, and return the flags from the TCP header in the packet data."""
	tcp_header_offset = get_tcp_header_offset(packet_data)
	flags = int.from_bytes(packet_data[tcp_header_offset+12:tcp_header_offset+14], byteorder='big') # Mask to get the lower 9 bits
	flag_names = ["FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR", "NS"]
	flag_status = {flag_names[i]: bool(flags & (1 << i)) for i in range(9)} # Map each flag name to its corresponding bit
	return flag_status

def get_timestamp(packet_header):
	"""Return the timestamp of the packet in seconds."""
	ts_sec = int.from_bytes(packet_header[:4], byteorder=config.endianness)
	ts_usec = int.from_bytes(packet_header[4:8], byteorder=config.endianness)
	return ts_sec + (ts_usec / 1000000)

def get_message_length(packet_data):
	"""Calculate and return the length of the message in bytes."""
	datagram_length_bytes = int.from_bytes(packet_data[config.IPV4_HEADER_OFFSET+2:config.IPV4_HEADER_OFFSET+4], byteorder='big')
	ip_header_length_bytes = (packet_data[config.IPV4_HEADER_OFFSET] & 0x0F) * 4
	tcp_header_offset = get_tcp_header_offset(packet_data)
	tcp_header_length_bytes = ((packet_data[tcp_header_offset+12] & 0xF0) >> 4) * 4
	return datagram_length_bytes - ip_header_length_bytes - tcp_header_length_bytes

def get_window_size(packet_data):
	"""Extract and return the window size from the packet data."""
	tcp_header_offset = get_tcp_header_offset(packet_data)
	return int.from_bytes(packet_data[tcp_header_offset+14:tcp_header_offset+16], byteorder='big')
