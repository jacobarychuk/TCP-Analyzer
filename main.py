import sys

def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header

		magic_number = int.from_bytes(global_header[:4], byteorder='big') # Extract the magic_number field and convert to an int with big-endian byte ordering

		if magic_number == 0xa1b2c3d4: # File was written in big-endian format
			endianness = 'big'
		elif magic_number == 0xd4c3b2a1: # File was written in little-endian format
			endianness = 'little'
		else:
			print("Unsupported file format", file=sys.stderr)
			sys.exit(1)
		
		print("Endianness:", endianness)

if __name__ == "__main__":
	main()
