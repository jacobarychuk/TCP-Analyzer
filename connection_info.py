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
		self.packet_count_source_destination = 0
		self.packet_count_destination_source = 0
		self.byte_count_source_destination = 0
		self.byte_count_destination_source = 0
		self.window_sizes = []

	def add_packet(self, packet_header, packet_data, direction):
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
		# Update packet and byte counts based on direction
		if direction == 'forward':
			self.packet_count_source_destination += 1
			self.byte_count_source_destination += get_message_length(packet_data)
		if direction == 'reverse':
			self.packet_count_destination_source += 1
			self.byte_count_destination_source += get_message_length(packet_data)
		# Retrieve window size and store in list
		window_size = get_window_size(packet_data)
		self.window_sizes.append(window_size)

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

	def get_packet_count_source_destination(self):
		"""Return the number of packets sent from the source to the destination."""
		return self.packet_count_source_destination

	def get_packet_count_destination_source(self):
		"""Return the number of packets sent from the destination to the source."""
		return self.packet_count_destination_source

	def get_packet_count(self):
		"""Return the total number of packets."""
		return self.packet_count_source_destination + self.packet_count_destination_source

	def get_byte_count_source_destination(self):
		"""Return the number of bytes sent from the source to the destination."""
		return self.byte_count_source_destination

	def get_byte_count_destination_source(self):
		"""Return the number of bytes sent from the destination to the source."""
		return self.byte_count_destination_source

	def get_byte_count(self):
		"""Return the total number of bytes."""
		return self.byte_count_source_destination + self.byte_count_destination_source
