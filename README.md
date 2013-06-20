WatchFolder
===========



Features
--------

[watchdog](https://github.com/gorakhargosh/watchdog) is used to get system events.

* folders monitoring
* file sequence and video treatment



Installation
------------

[setuptools](https://pypi.python.org/pypi/setuptools/0.7.2) installation :

    python setup.py install



Simple usage example
--------------------

configuration.conf :

```conf
[conf]
module = allcallbacks
[.dpx]
callback = fun_dpx
delay = 10
[.mov]
callback = fun_mov
delay = 5
```

allcallbacks.py :

```python
#!/usr/bin/env python


def fun_dpx(file_path):
    print 'Something to do with dpx file :', file_path


def fun_mov(file_path):
    print 'Something to do with mov file :', file_path
```

sample.py :

```python
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
```
