#!/usr/bin/env python
import sys
import time
import os.path
import argparse
import logging
from monitor import Monitor

parser = argparse.ArgumentParser( description='Watch Folder')
parser.add_argument(
	'-d', '--directory', default=".",
	help='watched directory')
parser.add_argument(
	'-c', '--configuration', default="configuration.conf",
	help='set the configuration file')
parser.add_argument(
		'-l', '--log', default="WARNING",
		help='set the verbose level (critical, error, warning, info, debug)')

args = parser.parse_args()

numeric_level = getattr( logging, args.log.upper(), None)
if not isinstance( numeric_level , int):
	print ( 'Invalid log level: %s' % args.log.upper() )
	print ( 'select one of these:' )
	print ( ' - critical' )
	print ( ' - error' )
	print ( ' - warning' )
	print ( ' - info' )
	print ( ' - debug' )
	exit()

logging.basicConfig(
	#filename='example.log',
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%m/%d/%Y %H:%M:%S',
	level = numeric_level
	)

if not os.path.isdir( args.directory ):

	logging.critical( " Could not start watching not on existing directory" )
	exit( -1 )

monitor = Monitor( args.directory )
monitor.load_conf( args.configuration )
monitor.start()

logging.info( " start watching : " + monitor._path )

try:
	while True:
		time.sleep( 10 )
except KeyboardInterrupt:
	logging.info( " stop watching : " + monitor._path )
	monitor.stop()

logging.info( " exit for folder : " + monitor._path )
