import os

def test():
	path = os.path.abspath(__file__)
	dir = os.path.dirname(path)
	print(path,dir)
