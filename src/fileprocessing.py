from interface import AbstractFileProcessing, Trie
import os
import json
import pickle
import py
from pypinyin import lazy_pinyin
from tqdm import tqdm


class Officialfpcs(AbstractFileProcessing):
	'''
		2016-xx.txt
		generate trans.pkl emit.pkl start.pkl
		n-gram
	'''
	def __init__(self):
		AbstractFileProcessing.__init__(self)
		self.fns = ['2016-02-py2sen.json','2016-04-py2sen.json','2016-05-py2sen.json','2016-06-py2sen.json','2016-07-py2sen.json','2016-08-py2sen.json','2016-09-py2sen.json','2016-10-py2sen.json','2016-11-py2sen.json']
		self.chars_set = self.readpkl("chars.pkl")
	def count(self,n = 1):
		count = self.readpkl("hz-count-" + str(n) +".pkl")
		for fn in self.fns:
			print(fn + " processing...")
			print("file loading...")
			objs = self.readjson(fn)
			for i in tqdm(range(len(objs))):
				pinyin = objs[i][0]
				hanzi = objs[i][1]
				for j in range(len(hanzi[:-n])):
					flag = False
					for k in range(n):
						if hanzi[j + k] not in self.chars_set:
							flag = True
							break
					if flag: continue
					key = hanzi[j:j + n]
					if key not in count.keys():
						count[key] = 0
					count[key] = count[key] + 1
		self.writepkl(count,"hz-count-" + str(n) + ".pkl")
					
	def trans_1(self):
		trans_1_n = self.readpkl("trans-1-n.pkl")
	
		for fn in self.fns:
			print(fn + " processing...")
			print("file loading...")
			objs = self.readjson(fn)
			for i in tqdm(range(len(objs))):
				pinyin = objs[i][0]
				hanzi = objs[i][1]
				for j,hz in enumerate(hanzi[:-1]):
					if hz not in self.chars_set or hanzi[j + 1] not in self.chars_set: continue
					if hz not in trans_1_n.keys():
						trans_1_n[hz] = {}
					if hanzi[j + 1] not in trans_1_n[hz].keys():
						trans_1_n[hz][hanzi[j + 1]] = 0
					trans_1_n[hz][hanzi[j + 1]] = trans_1_n[hz][hanzi[j + 1]] + 1
		self.writepkl(trans_1_n,"trans-1-n.pkl")

		#prob
		print("prob processing...")
		for hz1 in trans_1_n.keys():
			total = 0.0
			for hz2 in trans_1_n[hz1].keys():
				total = total + trans_1_n[hz1][hz2]
			for hz2 in trans_1_n[hz1].keys():
				trans_1_n[hz1][hz2] = trans_1_n[hz1][hz2] / total
		self.writepkl(trans_1_n,"trans-1-p.pkl")

	def trans_2(self):
		trans_2_n = self.readpkl("trans-2-n.pkl")
		for fn in self.fns:
			print(fn + " processing...")
			print("file loading...")
			objs = self.readjson(fn)
			for i in tqdm(range(len(objs))):
				pinyin = objs[i][0]
				hanzi = objs[i][1]
				for j,hz in enumerate(hanzi[:-2]):
					if hz not in self.chars_set or hanzi[j + 1] not in self.chars_set or hanzi[j + 2] not in self.chars_set: continue
					if hz not in trans_2_n.keys():
						trans_2_n[hz] = {}
					if hanzi[j + 1] not in trans_2_n[hz].keys():
						trans_2_n[hz][hanzi[j + 1]] = {}
					if hanzi[j + 2] not in trans_2_n[hz][hanzi[j + 1]].keys():
						trans_2_n[hz][hanzi[j + 1]][hanzi[j + 2]] = 0
					trans_2_n[hz][hanzi[j + 1]][hanzi[j + 2]] = trans_2_n[hz][hanzi[j + 1]][hanzi[j + 2]] + 1 

		self.writepkl(trans_2_n,"trans-2-n.pkl")

		#prob
		print("prob processing...")
		for hz1 in trans_2_n.keys():
			for hz2 in trans_2_n[hz1].keys():
				total = 0.0
				for hz3 in trans_2_n[hz1][hz2].keys():
					total = total + trans_2_n[hz1][hz2][hz3]
				for hz3 in trans_2_n[hz1][hz2].keys():
					trans_2_n[hz1][hz2][hz3] = trans_2_n[hz1][hz2][hz3] / total
		self.writepkl(trans_2_n,"trans-2-p.pkl")

				
	
	def position(self):
		'''info of position'''
		pass


	def emit_1(self):
		#done
		pass
	def emit_2(self):
		emit_2_n = self.readpkl("emit-2-n.pkl")
		for fn in self.fns:
			print(fn + " processing...")
			print("file loading...")
			objs = self.readjson(fn)
			for i in tqdm(range(len(objs))):
				pinyin = objs[i][0]
				hanzi = objs[i][1]
				for j,hz in enumerate(hanzi[:-1]):
					if hz not in self.chars_set or hanzi[j + 1] not in self.chars_set: continue
					if hz not in emit_2_n.keys():
						emit_2_n[hz] = {}
					if hanzi[j + 1] not in emit_2_n[hz].keys():
						emit_2_n[hz][hanzi[j + 1]] = {}
					if pinyin[j + 1] not in emit_2_n[hz][hanzi[j + 1]]:
						emit_2_n[hz][hanzi[j + 1]][pinyin[j + 1]] = 0
					emit_2_n[hz][hanzi[j + 1]][pinyin[j + 1]] = emit_2_n[hz][hanzi[j + 1]][pinyin[j + 1]] + 1
		self.writepkl(emit_2_n,"emit-2-n.pkl")
		
		#prob
		print("prob processing...")
		for hz1 in emit_2_n.keys():
			for hz2 in emit_2_n[hz1].keys():
				total = 0.0
				for py in emit_2_n[hz1][hz2].keys():
					total = total + emit_2_n[hz1][hz2][py]
				for py in emit_2_n[hz1][hz2].keys():
					emit_2_n[hz1][hz2][py] = emit_2_n[hz1][hz2][py] / total	
		self.writepkl(emit_2_n,"emit-2-p.pkl")
		
	
	def process(self):
		#self.trans_1()
		#self.trans_2()
		#self.emit_2()
		self.count(3)


class Corpusfpcs(AbstractFileProcessing):
	def __init__(self):
		AbstractFileProcessing.__init__(self)
		self.trie = Trie() 
	def words(self):
		objs = self.readpkl("words.pkl")
		keys = list(objs.keys())
		for k in keys:
			py = lazy_pinyin(k)
			self.trie.add(k,py)
		self.writepkl(self.trie.root,"trie.pkl")
	def process(self):
		self.words()

