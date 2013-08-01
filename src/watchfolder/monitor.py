#!/usr/bin/env python

import time
import threading
import ConfigParser
import FileInstance
import logging
import types
import os

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import *

class Monitor( FileSystemEventHandler ):
	def __init__(self, recursive=False):
		self._path = None
		self._callbacks = dict()
		self._delays = dict()
		self._is_recursive = recursive
		self._files = list()
		self._thread = None
		self._stop_event = None
		self._observer = None
		

	def loop(self):
		while not self._stop_event.isSet():
			for f in self._files[:]:
				try:
					with open(f.path, 'r') as opened:
						if f.elapsed_time() > f.delay:
							f.launch()
							os.renames(f.path, os.path.join(self._path, 
											'.process', 
											os.path.basename(f.path)))
							logging.debug("In file processing (\"%s\") - File processed and moved into .process", f.path)
							self._files.remove(f)
				except IOError as e:
					if e.errno == 26:
						f.set_modification()
						logging.debug("In file processing (\"%s\") - File modified (busy)", f.path)
					else:
						logging.debug("In file processing (\"%s\") - %s", f.path, str(e))
					
			self._stop_event.wait(1)
		self._observer.join()


	def load_conf(self, configurationFile):
		conf = ConfigParser.ConfigParser()
		conf.read(configurationFile)
		
		try:
			path = conf.get('conf', 'path')
			self.set_path_to_watch(path)

			module = __import__(conf.get('conf', 'module'))
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

	def set_path_to_watch(self, path):
		if (not os.access(path, os.R_OK)) or (not os.access(path, os.W_OK)):
			logging.error("Monitor - The specified path is not an available directory (\"%s\")", path)
			return
		
		self._path = os.path.abspath(path)
		

	def add_extension_options(self, extension, callback, delay):
		if isinstance(extension, str) and isinstance(callback, types.FunctionType) and isinstance(delay, int):
			self._callbacks[extension] = callback
			self._delays[extension] = delay
			

	def start(self):
		logging.info("Monitor - Starting")

		if self._path == None:
			logging.error("Monitor - Can't start: no directory specified")
			return

		self._thread = threading.Thread( None, self.loop )
		self._stop_event = threading.Event()
		self._observer = Observer()
		self._observer.schedule(self,
					self._path,
					recursive = self._is_recursive)

		self._observer.start()
		self._thread.start()


	def stop(self):
		logging.info("Monitor - Stopping")

		try:
			self._observer.stop()
			self._stop_event.set()
			self._thread.join()
		except:
			pass

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

			self._files.append( FileInstance.FileInstance(path,
								self._callbacks[tmp],
								self._delays[tmp]))
		else:
			logging.warning("In file processing (\"%s\") - No option for this extension", path)

	
	def parse_directory(self):
		if (not self._path):
			return

		logging.info("Monitor - Parse the directory to watch")		

		for f in os.listdir(self._path):
			filePath = os.path.join(self._path, f)
			self.on_created(FileCreatedEvent(filePath))


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
