import os

def dpxProcessor( filePath ):
	logging.info("REMOVING .DPX FILE: %s", filePath)
	os.remove( filePath )

def movProcessor( filePath ):
	logging.info("REMOVING .MOV FILE: %s", filePath)
	os.remove( filePath )
