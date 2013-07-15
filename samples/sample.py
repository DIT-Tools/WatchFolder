#!/usr/bin/env python

import sys
import time
import os.path
import argparse
import logging
import logging.handlers

from monitor import Monitor

class Filter(object):

	def __init__(self, level):
		self._level = level

	def filter(self, logRecord):
		return logRecord.levelno <= self._level


def configure_root_logger( level ):
	root_logger = logging.getLogger()
	root_logger.setLevel( logging.DEBUG )

	formatter = logging.Formatter( '%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %H:%M:%S' )

	handler = logging.handlers.RotatingFileHandler( 'watchFolder.log', 'a', 1000000, 1 )
	handler.addFilter( Filter( logging.CRITICAL ) )
	handler.setFormatter( formatter )
	root_logger.addHandler( handler )

	stdout = logging.StreamHandler()
	stdout.addFilter( Filter( level ) )
	stdout.setFormatter( formatter )
	root_logger.addHandler( stdout )


def configure_args_parser():
	parser = argparse.ArgumentParser(description='Watch Folder')

	parser.add_argument(
		'configFiles',
		help  = 'set the configuration files',
		nargs = '+'
	)

	parser.add_argument(
		'-l', '--log',
		default = "CRITICAL",
		choices = [ 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG' ],
		help    = 'set the verbose level'
	)

	return parser


if __name__ == '__main__':
	parser = configure_args_parser()
	args = parser.parse_args()
	level = getattr( logging, args.log, None )
	configure_root_logger( level )

	monitorsList = list()
	for configFile in args.configFiles:
		monitorsList.append( Monitor() )
		monitorsList[-1].load_conf( configFile )
		monitorsList[-1].start()

	try:
		while True:
			time.sleep( 1 )
	except KeyboardInterrupt:
		for monitor in monitorsList:
			monitor.stop()

