import json
import os
import pickle
def encode(word,residue_py_list):
	code = word
	for py in residue_py_list:
		code = code + py
	return code

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
	

class Trie(AbstractFileWR):
	'''prefix'''
	def __init__(self,init = False):
		self.end = '\n'
		if init: self.root = {'py':'','hz':'','next':{},'end':''}
		else:
			self.root = self.readpkl("trie.pkl")
	def add(self,hz,py):
		'''add a string'''
		node = self.root
		for (h,p) in zip(hz,py):
			code = encode(h,p)
			if code not in node['next'].keys():
				node['next'][code] = {'py':p,'hz':h,'next':{},'end':''}
			node = node['next'][code]
		node['end'] = self.end
	def search(self,py):
		res = self.__search(py,self.root,0,'')
		return res
	def cat(self,d1,d2):
		'''d1:{len1:[],len2:[]}
			d2:{len1:[],len2:[]}
		'''
		for k,v in d2.items():
			if k not in d1.keys():
				d1[k] = v
			else:
				d1[k] = d1[k] + v
		return d1

	def __search(self,py,node,index,prefix):
		res = {}
		#{len1:[hz,hz,..],len2:[],len3:[]}
		if index >= len(py): return res
		for k in node['next'].keys():
			if py[index] == node['next'][k]['py']:
				_res = self.__search(py,node['next'][k],index + 1,prefix + node['next'][k]['hz'])
				res = self.cat(res,_res)

				if node['next'][k]['end'] == self.end:
					item = prefix + node['next'][k]['hz']
					length = len(item)
					if length not in res.keys():
						res[length] = [item]
					else:
						res[length] = res[length] + [item]
		return res




		
		