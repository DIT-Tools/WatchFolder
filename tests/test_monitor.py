#!/usr/bin/env python


import os
import time
from nose.tools import *
from monitor import Monitor        


class TestMonitor(object):
    
    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        pass

    def setUp(self):
        pass

    def teardown(self):
        pass

    def test_load_conf(self):
        monitor = Monitor('.')
        monitor.load_conf('configuration.conf')
        module = __import__('callbacks')
        eq_('*' in monitor._callbacks, True)
        eq_('.mov' in monitor._callbacks, True)
        eq_('.dpx' in monitor._callbacks, False)
        eq_('.gif' in monitor._callbacks, False)
        eq_('.jpg' in monitor._callbacks, False)
        eq_('.png' in monitor._callbacks, False)
        eq_('*' in monitor._delays, True)
        eq_('.mov' in monitor._delays, True)
        eq_('.dpx' in monitor._delays, False)
        eq_('.gif' in monitor._delays, False)
        eq_('.jpg' in monitor._delays, False)
        eq_('.png' in monitor._delays, False)
        eq_(getattr(module, 'allProcessor'), monitor._callbacks['*'])
        eq_(getattr(module, 'movProcessor'), monitor._callbacks['.mov'])
        eq_(10, monitor._delays['*'])
        eq_(5, monitor._delays['.mov'])

    @timed(10)
    def test_start_stop(self):
        monitor = Monitor('.')
        monitor.load_conf('configuration.conf')
        monitor.start()
        eq_(0, len(monitor._files))
        f = open('tmp.mov', 'w')
        f.write('0123456789abcdef')
        f.close()
        monitor.stop()
        time.sleep(3)
        monitor.start()
        eq_(1, len(monitor._files))
        time.sleep(2)
        monitor.stop()
        os.remove('tmp.mov')
