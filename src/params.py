import json
import math
from interface import AbstractParams,Trie


class hmm1Params(AbstractParams):
	''' viterbi parameters loaded '''
	def	__init__(self,smoother):
		self.minprob = 1e-200
		self.py2hz_dict = self.readpkl("py2hz-p.pkl")
		#self.trans_dict = self.readpickle("trans-1-p.pkl")
		self.emit_dict = self.readpkl("emit-1-p.pkl")
		self.c1 = self.readpkl("hz-count-1.pkl")
		self.c2 = self.readpkl("hz-count-2.pkl")
		self.smoother = smoother
		smoother.setting(self.c1,self.c2,None,self.py2hz_dict)

	def get_states(self,py):
		return list(self.py2hz_dict[py].keys())
		
	def start(self,py,hz):
		# P(hz | py)
		if hz not in self.py2hz_dict[py].keys():
			return self.minprob 
		return max(self.py2hz_dict[py][hz],self.minprob)

	def trans(self,prev_s,cur_s):
		''' #based on trans_dict
		if prev_s not in self.trans_dict.keys() or cur_s not in self.trans_dict[prev_s].keys():
			return self.minprob
		return max(self.trans_dict[prev_s][cur_s],self.minprob)
		'''
		#self.c1/c2
		return self.smoother.smooth2(prev_s,cur_s)
			

	def emit(self,obs,state):
		# P(py | hz)
		if state not in self.emit_dict.keys() or obs not in self.emit_dict[state].keys():
			return self.minprob
		return max(self.emit_dict[state][obs],self.minprob)
		
class hmm2Params(hmm1Params):
	def __init__(self,smoother):
		hmm1Params.__init__(self,smoother)
		#self.trans_2_dict = self.readpickle("trans-2-p.pkl")
		self.c3 = self.readpkl("hz-count-3.pkl")
		self.emit_2_dict = self.readpkl("emit-2-p.pkl")
		self.smoother.setting(c3 = self.c3)
	def trans2(self,s1,s2,s3):
		'''
		if s1 not in self.trans_2_dict.keys() or s2 not in self.trans_2_dict[s1].keys() or s3 not in self.trans_2_dict[s1][s2].keys():
			return self.minprob
		return max(self.trans_2_dict[s1][s2][s3],self.minprob)
		'''
		return self.smoother.smooth3(s1,s2,s3)
	def emit2(self,s1,s2,obs):
		if s1 not in self.emit_2_dict.keys() or s2 not in self.emit_2_dict[s1].keys() or obs not in self.emit_2_dict[s1][s2].keys():
			return self.minprob 
		return self.emit_2_dict[s1][s2][obs]
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

class dagParams(AbstractParams):
	def __init__(self):
		print("model loading...")
		self.c1 = self.readpkl("word-all-1-n.pkl")
		self.c2 = self.readpkl("word-filter-alter-2-n.pkl")
		self.py2hz_dict = self.readpkl("py2hz-p.pkl")
		self.trie = Trie()
		print("model loaded")
	def search_prefix(self,py_list):
		return self.trie.search(py_list)
	def get_states(self,py):
		return list(self.py2hz_dict[py].keys())
	def trans(self,prev_w,next_w):
		if prev_w == '':
			#return 1 
			if next_w not in self.c1.keys():
				return math.pow(1e-200,1e-4)
			else: return math.pow(max(1e-200,self.c1[next_w] / 271134122),1e-4)
		if next_w == '':
			#return 1
			if prev_w not in self.c1.keys():
				return math.pow(1e-200,1e-4)
			else: return math.pow(max(1e-200,self.c1[prev_w] / 271134122),1e-4)

		w2 = prev_w + next_w
		if w2 not in self.c2.keys():
			c2_num = 0
		else: c2_num = self.c2[w2]
		if next_w not in self.c1.keys():
			c1_num = 0
		else: c1_num = self.c1[next_w]
		return max(1e-200, (1-1e-100) * c2_num / max(c1_num,1,c2_num) + (1e-100) * c1_num /355584657)
		