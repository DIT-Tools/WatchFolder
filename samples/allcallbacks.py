import os

def dpxProcessor( file_path ):
	print( "[EVENT]   removing dpx file : " + file_path )
	os.remove( file_path )

def movProcessor( file_path ):
	print( "[EVENT]   removing mov file : "+ file_path )
	os.remove( file_path )
