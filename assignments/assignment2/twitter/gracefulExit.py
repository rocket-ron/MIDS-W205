import sys
import signal

# Graceful exit signal handler - handle a CTRL-C interrupt
class GracefulExit:
	def __enter__(self):
		self.SIGINT = signal.getsignal(signal.SIGINT)

	def __exit__(self, type, value, traceback):
		signal.signal(signal.SIGINT, self.SIGINT)

