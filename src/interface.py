import json
import os
import pickle

class AbstractFileWR(object):
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


class AbstractParams(AbstractFileWR):

	def getParamsDict(self):
		pass


class AbstractFileProcessing(AbstractFileWR):
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


class AbstractSmooth(AbstractFileWR):
	def __init__(self):
		self.config = self.readjson("config.json")
		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.py2hz_p = None
	def setting(self,c1 = None,c2 = None,c3 = None,py2hz_p = None):
		'''called by params'''
		if self.c1 == None: self.c1 = c1
		if self.c2 == None: self.c2 = c2
		if self.c3 == None: self.c3 = c3
		if self.py2hz_p == None: self.py2hz_p = py2hz_p	

	def smooth2(self,s1,s2):
		'''2 order smooth
			P(s2|s1)
		'''
		pass
	def smooth3(self,s1,s2,s3):
		'''3 order smooth
			P(s3|s1,s2)
		'''
		pass
	