import sys

def get_endianness(global_header):

	magic_number = int.from_bytes(global_header[:4], byteorder='big') # Extract magic_number from global header

	if magic_number == 0xa1b2c3d4: # File was written in big-endian format
		return 'big'
	elif magic_number == 0xd4c3b2a1: # File was written in little-endian format
		return 'little'
	else:
		print("Unsupported file format", file=sys.stderr)
		sys.exit(1)
