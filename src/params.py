import json
from config import Config as cfg
from interface import AbstractParams


class viterbiParams(AbstractParams):
	''' viterbi parameters loaded '''
	def	__init__(self,minprob = 1e-200):
		self.minprob = minprob
		self.py2hz_dict = self.readpickle(cfg.py2hz_name)
		self.trans_dict = self.readpickle(cfg.trans_name)
		self.emit_dict = self.readpickle(cfg.emit_name)

	def get_states(self,py):
		return list(self.py2hz_dict[py].keys())
		
	def start(self,py,hz):
		# P(hz | py)
		return max(self.py2hz_dict[py][hz],self.minprob)

	def trans(self,prev_s,cur_s):
		if cur_s not in self.trans_dict[prev_s].keys(): return self.minprob
		return max(self.trans_dict[prev_s][cur_s],self.minprob)

	def emit(self,py,hz):
		# P(py | hz)
		return max(self.emit_dict[hz][py],self.minprob)
		
