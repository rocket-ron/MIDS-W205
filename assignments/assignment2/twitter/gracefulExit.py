import sys
import signal

# Graceful exit signal handler
class GracefulExit:
	def __enter__(self):
		self.SIGINT = signal.getsignal(signal.SIGINT)

	def __exit__(self, type, value, traceback):
		signal.signal(signal.SIGINT, self.SIGINT)

