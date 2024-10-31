from utils import *

class ConnectionInfo:

	capture_start_time = None

	def __init__(self):
		"""Initialize a new ConnectionInfo instance with default values."""
		self.syn_count = 0
		self.fin_count = 0
		self.reset = False
		self.start_time = None
		self.end_time = None

	def add_packet(self, packet_header, packet_data):
		"""Process a packet and update the connection information."""
		# Retrieve flags from TCP header and update connection status
		flags = get_flags(packet_data)
		self.update_status(flags)
		# Retrieve timestamp and update times
		timestamp = get_timestamp(packet_header)
		if ConnectionInfo.capture_start_time is None:
			ConnectionInfo.capture_start_time = timestamp
		if self.start_time is None:
			self.start_time = timestamp - ConnectionInfo.capture_start_time	
		if flags["FIN"]:
			self.end_time = timestamp - ConnectionInfo.capture_start_time

	def update_status(self, flags):
		"""Update the connection status based on the flags in the TCP header."""
		if flags["RST"]: self.reset = True
		if flags["SYN"]: self.syn_count += 1
		if flags["FIN"]: self.fin_count += 1

	def get_status(self):
		"""Return a string representation of the status for the connection."""
		return f"S{self.syn_count}F{self.fin_count}{'/R' if self.reset else ''}"

	def get_start_time(self):
		"""Return the start time of the connection rounded to 6 decimal places."""
		if self.start_time is None:
			return None
		return round(self.start_time, 6)

	def get_end_time(self):
		"""Return the end time of the connection rounded to 6 decimal places."""
		if self.end_time is None:
			return None
		return round(self.end_time, 6)

	def get_duration(self):
		"""Return the difference between the start time and end time of the connection rounded to 6 decimal places."""
		if self.start_time is None or self.end_time is None:
			return None
		return round(self.end_time - self.start_time, 6)
