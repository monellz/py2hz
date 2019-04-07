from viterbi import viterbi, viterbi2
import params,smooth
import json

class Checker:
	def __init__(self,param,algo):
		self.param = param
		self.algo = algo
	def singlepredict(self,py,res_num = 5):
		res = self.algo(self.param,py)
		return res[:res_num]
	def predict(self,pybatch):
		res = []
		for py in pybatch:
			res.append(self.singlepredict(py,1))
		return res
	def evaluate(self,pybatch,hzbatch):
		eval = {} #dict  acc:  complete acc:
		acc_num = 0
		acc_total = 0
		cacc_num = 0
		cacc_total = 0
		total_res = []
		for (py,hz) in zip(pybatch,hzbatch):
			res = self.singlepredict(py,1)
			if res == hz:
				cacc_num = cacc_num + 1
			cacc_total = cacc_total + 1
			for i in range(len(hz)):
				if res[i] == hz[i]: acc_num = acc_num + 1
				acc_total = acc_total + 1
			total_res.append(res)

		eval['acc'] = acc_num / acc_total
		eval['complete acc'] = cacc_num / cacc_total
		return total_res, eval 

			
smoother = smooth.Adddelta()
#smoother = smooth.Linear()
hmm1p = params.hmm1Params(smoother)
hmm2p = params.hmm2Params(smoother)
checker = Checker(hmm2p,viterbi2)

while True:
	print("input:",end='')
	text = input().strip().split(' ')
	print(text)
	res = checker.singlepredict(text)
	print(res)
