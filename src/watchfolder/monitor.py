#!/usr/bin/env python

import time
import threading
import ConfigParser
import FileInstance
import logging
import types
from watchdog.observers import *
from watchdog.events import *

class Monitor( FileSystemEventHandler ):
	def __init__( self, path, recursive = False ):
		self._path = path
		self._callbacks = dict()
		self._delays = dict()
		self._is_recursive = recursive
		self._thread = threading.Thread( None, self.loop )
		self._stop_event = threading.Event()
		self._observer = Observer()
		self._files = list()
		self._observer.schedule( self,
					 self._path,
					 recursive = self._is_recursive )

	def loop(self):
		while not self._stop_event.isSet():
			for f in self._files[:]:
				if f.elapsed_time() > f.delay:
					f.launch()
					self._files.remove(f)
			self._stop_event.wait(1)
		self._observer.join()


	def load_conf(self, configurationFile):
		conf = ConfigParser.ConfigParser()
		conf.read( configurationFile )
		
		try:
			module = __import__( conf.get( 'conf', 'module' ) )
		except Exception as e:
			logging.error( "In config file (\"%s\") - %s", configurationFile, e.message)
			return 
			
		for section in conf.sections():
			if section == 'conf':
				continue

			try:
				callback = getattr(module, conf.get(section, 'callback'))
				delay = conf.getint(section, 'delay')
				
				self.add_extension_options(section, callback, delay)
			except Exception as e:
				logging.warning( "In config file (\"%s\") - %s", configurationFile, e.message)
				continue


	def add_extension_options(self, extension, callback, delay):
		if isinstance(extension, str) and isinstance(callback, types.FunctionType) and isinstance(delay, int):
			self._callbacks[extension] = callback
			self._delays[extension] = delay
			

	def start( self ):
		logging.info("Monitor - Starting")

		self._observer.start()
		self._thread.start()


	def stop( self ):
		logging.info("Monitor - Stopping")

		self._observer.stop()
		self._stop_event.set()
		self._thread.join()


	def on_created( self, e ):
		if e.is_directory:
			return

		path = e.src_path
		tmp = None

		for key in self._callbacks.keys():
			if key == '.*' or key == '*':
				tmp = key
				
			elif path.endswith(key):
				tmp = key	
				break

		if tmp:
			logging.debug("In file processing (\"%s\") - File created", path)

			self._files.append(FileInstance.FileInstance(path,
								     self._callbacks[tmp],
								     self._delays[tmp]))
		else:
			logging.warning("In file processing (\"%s\") - No option for this extension", path)


	def on_modified( self, e ):
		if e.is_directory:
			return

		for f in self._files:
			if e.src_path == f.path:
				logging.debug("In file processing (\"%s\") - File modified", f.path)
				f.set_modification()
				break


	def on_moved( self, e ):
		pass


	def on_deleted( self, e ):
		pass
