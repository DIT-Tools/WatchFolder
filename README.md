WatchFolder
===========



Features
--------

[watchdog](https://github.com/gorakhargosh/watchdog) is used to get system events.

* folders monitoring
* file sequence and video treatment



Simple usage example
--------------------

    #!/usr/bin/env python


    import time
    from monitor import Monitor


    def callback(file_path):
        '''Callback function

        file_path : absolute path of a completed file

        This function will be call by the Monitor instance each time a file
        is completed.

        '''
        print file_path, 'is completed !'


    monitor = Monitor('.', callback)  # Monitor cur directory
    monitor.start()                   # Start thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
    monitor.stop()                    # Stop thread and wait until it terminates
    print 'All is over !'



Installation
------------

[setuptools](https://pypi.python.org/pypi/setuptools/0.7.2) installation :

    python setup.py install
