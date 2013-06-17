#!/usr/bin/env python


import time
import threading
from watchdog.observers import *
from watchdog.events import *


class FileInstance(object):

    def __init__(self, path):
        self._path = path
        self._modification_time = time.time()

    @property
    def path(self):
        return self._path

    @property
    def modification_time(self):
        return self._modification_time

    def set_modification(self):
        self._modification_time = time.time()

    def elapsed_time(self):
        return time.time() - self._modification_time


class Monitor(FileSystemEventHandler):

    def __init__(self, path, callback, recursive = False, delay = 1.0):       
        self._thread = threading.Thread(None, self._loop)
        self._stop_event = threading.Event()
        self._observer = Observer()
        self._path = path
        self._callback = callback
        self._is_recursive = recursive
        self._delay = delay
        self._files = []        
        self._observer.schedule(self,
                                self._path,
                                recursive = self._is_recursive)

    def _loop(self):        
        while not self._stop_event.isSet():
            for f in self._files[:]:
                if f.elapsed_time() > self._delay:
                    self._callback(f.path)
                    self._files.remove(f)
            self._stop_event.wait(1)            
        self._observer.join()

    def start(self):        
        self._observer.start()
        self._thread.start()

    def stop(self):        
        self._observer.stop()
        self._stop_event.set()
        self._thread.join()

    def on_created(self, e):
        if not e.is_directory:
            self._files.append(FileInstance(e.src_path))

    def on_modified(self, e):
        if not e.is_directory:
            flag = True
            for f in self._files:
                if e.src_path == f.path:
                    f.set_modification()
                    flag = False
                    break
            if flag:
                pass

    def on_moved(self, e):
        pass

    def on_deleted(self, e):
        pass
