from interface import AbstractFileProcessing
import os
import json
import pickle
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
		#todo
		pass


	def emit_1(self):
		pass
					
	def process(self):
		#self.trans_1()
		self.trans_2()
