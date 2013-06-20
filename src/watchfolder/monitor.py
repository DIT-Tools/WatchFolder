#!/usr/bin/env python


import time
import threading
import ConfigParser
from watchdog.observers import *
from watchdog.events import *


class FileInstance(object):

    def __init__(self, path, callback, delay):
        self._path = path
        self._delay = delay
        self._callback = callback
        self._modification_time = time.time()

    @property
    def path(self):
        return self._path

    @property
    def delay(self):
        return self._delay

    def set_modification(self):
        self._modification_time = time.time()

    def elapsed_time(self):
        return time.time() - self._modification_time

    def execute(self):
        try:
            self._callback(self._path)
        except:
            pass


class Monitor(FileSystemEventHandler):

    def __init__(self, path, recursive = False):
        self._path = path
        self._callbacks = dict()
        self._delays = dict()
        self._is_recursive = recursive
        self._thread = threading.Thread(None, self._loop)
        self._stop_event = threading.Event()
        self._observer = Observer()
        self._files = list()
        self._observer.schedule(self,
                                self._path,
                                recursive = self._is_recursive)

    def _loop(self):
        while not self._stop_event.isSet():
            for f in self._files[:]:
                if f.elapsed_time() > f.delay:
                    f.execute()
                    self._files.remove(f)
            self._stop_event.wait(1)
        self._observer.join()

    def load_conf(self, conf_file):
        conf = ConfigParser.ConfigParser()
        conf.read(conf_file)
        try:
            module = __import__(conf.get('conf', 'module'))
            for section in conf.sections()[:]:
                try:
                    callback = getattr(module, conf.get(section, 'callback'))
                    delay = conf.getint(section, 'delay')
                    self._callbacks[section] = callback
                    self._delays[section] = delay
                except:
                    continue
        except:
            pass

    def start(self):
        self._observer.start()
        self._thread.start()

    def stop(self):
        self._observer.stop()
        self._stop_event.set()
        self._thread.join()

    def on_created(self, e):
        if e.is_directory:
            return
        path = e.src_path
        for key in self._callbacks.keys():
            if path.endswith(key):
                self._files.append(FileInstance(path,
                                                self._callbacks[key],
                                                self._delays[key]))
                break

    def on_modified(self, e):
        if e.is_directory:
            return
        for f in self._files:
            if e.src_path == f.path:
                f.set_modification()
                flag = False
                break

    def on_moved(self, e):
        pass

    def on_deleted(self, e):
        pass
