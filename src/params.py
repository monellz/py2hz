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

	def emit(self,obs,state):
		# P(py | hz)
		if state not in self.emit_dict.keys() or obs not in self.emit_dict[state].keys():
			return self.minprob
		return max(self.emit_dict[state][obs],self.minprob)
		
class hmm2Params(hmm1Params):
	def __init__(self):
		hmm1Params.__init__(self)
		self.trans_2_dict = self.readpickle("trans-2-p.pkl")
		self.emit_2_dict = self.readpickle("emit-2-p.pkl")
	def trans2(self,s1,s2,s3):
		if s1 not in self.trans_2_dict.keys() or s2 not in self.trans_2_dict[s1].keys() or s3 not in self.trans_2_dict[s1][s2].keys():
			return self.minprob
		return max(self.trans_2_dict[s1][s2][s3],self.minprob)
	def emit2(self,s1,s2,obs):
		if s1 not in self.emit_2_dict.keys() or s2 not in self.emit_2_dict[s1].keys() or obs not in self.emit_2_dict[s1][s2].keys():
			return self.minprob
		return max(self.emit_2_dict[s1][s2][obs],self.minprob)
	'''
	def get_states(self,py):
		return super().get_states(py)
	def start(self,py,hz):
		return super().start(py,hz)
	def trans(self,prev_s,cur_s):
		return super().trans(prev_s,cur_s)
	def emit(self,py,hz):
		return super().emit(py,hz)
	'''
