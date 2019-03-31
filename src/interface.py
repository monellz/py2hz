import json
import os


class AbstractParams(object):
	def readjson(self,fname):
		dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.json(dir,'data',fname)) as f:
			data = json.load(f)
		return data
