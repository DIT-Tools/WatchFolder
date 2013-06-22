import time
import logging

class FileInstance( object ):
	def __init__( self, path, callback, delay ):
		self.path = path
		self.delay = delay
		self.callback = callback
		self.modificationTime = time.time()

	@property
	def path( self ):
		return self.path

	@property
	def delay( self ):
		return self.delay

	def set_modification( self ):
		self.modificationTime = time.time()

	def elapsed_time( self ):
		return time.time() - self.modificationTime

	def launch( self ):
		try:
			self.callback( self._path )
		except:
			logging.error( "could not launch " + self.path )
			pass
