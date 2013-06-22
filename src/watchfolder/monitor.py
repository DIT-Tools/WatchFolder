#!/usr/bin/env python

import time
import threading
import ConfigParser
import FileInstance
import logging
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

	def loop( self ):
		while not self._stop_event.isSet():
			for file in self._files[:]:
				if file.elapsed_time() > file.delay:
					file.launch()
					self._files.remove( file )
			self._stop_event.wait( 1 )
		self._observer.join()

	def load_conf( self, conf_file ):
		conf = ConfigParser.ConfigParser()
		conf.read( conf_file )
		try:
			module = __import__( conf.get( 'conf', 'module' ) )
			for section in conf.sections():
				if section == "conf":
					continue

				callback = ""
				try:
					callback = conf.get( section, 'callback' )
				except:
					logging.warning( " unable to found the callback in configuration file for " + section )
					continue

				try:
					self._callbacks[section] = getattr( module, callback )
				except:
					logging.error( " unable to found callback (" + callback + ") for " + section )
					continue

				try:
					delay = conf.getint( section, 'delay' )
				except:
					logging.warning( " set delay at 10 seconds for " + section )
					self._delays[section] = 10
		except:
			pass

	def start( self ):
		self._observer.start()
		self._thread.start()

	def stop( self ):
		self._observer.stop()
		self._stop_event.set()
		self._thread.join()

	def on_created( self, e ):
		if e.is_directory:
			return
		path = e.src_path
		for key in self._callbacks.keys():
			if path.endswith(key):
				self._files.append(
					FileInstance( path,
								  self._callbacks[ key ],
								  self._delays[ key ] ) )
				break

	def on_modified( self, e ):
		if e.is_directory:
			return
		for file in self._files:
			if e.src_path == file.path:
				file.set_modification()
				flag = False
				break

	def on_moved( self, e ):
		pass

	def on_deleted( self, e ):
		pass
