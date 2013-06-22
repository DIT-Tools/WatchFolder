import os
from setuptools import setup

def read(fname):
	return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()

setup(
	name             = 'WatchFolder',
	version          = '0.1.0',
	description      = ( 'Folder monitoring, file sequence and video treatment.' ),
	keywords         = 'watch folder video file sequence',
	packages         = [ 'watchfolder' ],
	long_description = read( 'README.md' ),
	install_requires = [ 'watchdog' ]
)
