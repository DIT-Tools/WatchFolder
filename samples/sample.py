#!/usr/bin/env python


import time
from monitor import Monitor


monitor = Monitor('.')
monitor.load_conf('configuration.conf')
monitor.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop()
print '\nAll is over !'
