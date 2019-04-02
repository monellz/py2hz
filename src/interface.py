import json
import os
import pickle


class AbstractParams(object):
	def readjson(self,fname):
		dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(dir,'data',fname)) as f:
			data = json.load(f)
		return data
	def readpickle(self,fname):
		dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(dir,'data',fname),"rb") as f:
			data = pickle.load(f)
		return data
		

	def getParamsDict(self):
		pass


class AbstractFileProcessing(object):
	def readpkl(self,fn):
		with open(self.absaddr(fn),"rb") as f:
			data = pickle.load(f)
		return data

	def writepkl(self,data,fn):
		with open(self.absaddr(fn),"wb") as f:
			pickle.dump(data,f)
	
	def readjson(self,fn):
		with open(self.absaddr(fn),"r") as f:
			data = json.load(f)
		return data

	def pwd(self):
		return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	def absaddr(self,fn):
		return os.path.join(self.pwd(),'data',fn)

	def openfile(self,fname,rmode,wmode):
		try:
			f = open(fname,rmode)
		except FileNotFoundError:
			print("not find",fname)
			print("creating...")
			f = open(fname,wmode)
		return f

	def process(self):
		'''file processing'''
		pass
