import os
import logging

def dpxProcessor( filePath ):
	logging.info("REMOVING .DPX FILE: %s", filePath)
	os.remove( filePath )

def movProcessor( filePath ):
	logging.info("REMOVING .MOV FILE: %s", filePath)
	os.remove( filePath )

def allProcessor(filePath):
	logging.info("ACTION FOR ALL OTHERS FILES: %s", filePath)
