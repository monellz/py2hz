import json
from Config import cfg
from interface import AbstractParams


Class viterbiParams(AbstractParams):
	''' viterbi parameters loaded '''
	def	__init__(self,minprop = 1e-200):
		self.minprop = minprop
		self.py2hz_dict = self.readjson(cfg.py2hz_name)
		self.trans_dict = self.readjson(cfg.trans_name)
		self.emit_dict = self.readjson(cfg.emit_name)

	def get_states(self,py):
		return self.py2hz_dict[py]
		
	def start(self,py,hz):
		# P(hz | py)
		return max(py2hz_dict[py][hz],self.minprop)

	def trans(self,prev_s,cur_s):
		return max(self.trans_dict[prev_s][cur_s],self.minprop)

	def emit(self,py,hz):
		return max(self.emit_dict[hz][py],self.minprop)
		
