import os

def dpxProcessor( filePath ):
	print "REMOVING .DPX FILE: %s", filePath
	os.remove( filePath )

def movProcessor( filePath ):
	print "REMOVING .MOV FILE: %s", filePath
	os.remove( filePath )

def allProcessor(filePath):
	print "ACTION FOR ALL OTHERS FILES: %s", filePath
