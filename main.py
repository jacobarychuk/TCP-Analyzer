import sys
import utils

def main():

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <filename>", file=sys.stderr)
		sys.exit(1)

	filename = sys.argv[1]

	with open(filename, 'rb') as f: # Open packet capture file for reading in binary mode

		global_header = f.read(24) # Read the first 24 bytes to get the global header
		endianness = utils.get_endianness(global_header)
		print("Endianness:", endianness)

if __name__ == "__main__":
	main()
