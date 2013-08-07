import os
import time
import logging

class FileInstance( object ):
	def __init__( self, path, callback, delay ):
		self._path = path
		self._delay = delay
		self._last_size = 0
		self._callback = callback
		self._modificationTime = time.time()

	@property
	def path( self ):
		return self._path

	@property
	def delay( self ):
		return self._delay

	@property
	def last_size( self ):
		return self._size

	def size_gap( self ):
		s = int(os.path.getsize(self._path))
		if s != self._last_size:
			self._last_size = s
			return True
		return False

	def set_modification( self ):
		self._modificationTime = time.time()

	def elapsed_time( self ):
		return time.time() - self._modificationTime

	def launch( self ):
		try:
			self._callback(self._path)
		except:
			logging.error("In file processing (\"%s\") - \'%s\' can't be launched", self._path, self._callback.__name__)
		else:
			logging.info("In file processing (\"%s\") - \'%s\' launched", self._path, self._callback.__name__)
