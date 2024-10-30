import sys

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
