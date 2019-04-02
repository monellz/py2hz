import json
from config import Config as cfg
from interface import AbstractParams


class hmm1Params(AbstractParams):
	''' viterbi parameters loaded '''
	def	__init__(self,minprob = 1e-200):
		self.minprob = minprob
		self.py2hz_dict = self.readpickle("py2hz-p.pkl")
		self.trans_dict = self.readpickle("trans-1-p.pkl")
		self.emit_dict = self.readpickle("emit-1-p.pkl")

	def get_states(self,py):
		return list(self.py2hz_dict[py].keys())
		
	def start(self,py,hz):
		# P(hz | py)
		if hz not in self.py2hz_dict[py].keys():
			return self.minprob 
		return max(self.py2hz_dict[py][hz],self.minprob)

	def trans(self,prev_s,cur_s):
		if prev_s not in self.trans_dict.keys() or cur_s not in self.trans_dict[prev_s].keys():
			return self.minprob
		return max(self.trans_dict[prev_s][cur_s],self.minprob)

	def emit(self,py,hz):
		# P(py | hz)
		if hz not in self.emit_dict.keys() or py not in self.emit_dict[hz].keys():
			return self.minprob
		return max(self.emit_dict[hz][py],self.minprob)
		
