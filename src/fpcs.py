from fileprocessing import  Officialfpcs as ofpcs
from fileprocessing import Corpusfpcs as cfpcs

def process(obj):
	obj.process()

if __name__ == '__main__':
	#obj = ofpcs()
	obj = cfpcs()
	process(obj)
