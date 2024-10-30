class ConnectionInfo:

	def __init__(self):
		"""Initialize a new ConnectionInfo instance with default values."""
		self.syn_count = 0
		self.fin_count = 0
		self.reset = False

	def update_status(self, flags):
		"""Update the connection status based on the flags in the TCP header."""
		if flags["RST"]: self.reset = True
		if flags["SYN"]: self.syn_count += 1
		if flags["FIN"]: self.fin_count += 1

	def get_status(self):
		"""Return a string representation of the status for the connection."""
		return f"S{self.syn_count}F{self.fin_count}{'/R' if self.reset else ''}"
