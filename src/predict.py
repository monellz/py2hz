from algorithm import viterbi, viterbi2,dp4word2
import params,smooth
import json, pickle
import getopt
import sys

class Checker:
	def __init__(self,param,algo):
		self.param = param
		self.algo = algo
	def singlepredict(self,py,res_num = 5):
		res = self.algo(self.param,py)
		return res[:min(len(res),res_num)]
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
		j = 0
		for (py,hz) in zip(pybatch,hzbatch):
			print(j,py,hz)
			j = j + 1
			py = py.strip().split(" ")
			res = self.singlepredict(py,1)
			#print(res)
			''' res = [(prob, hz)] '''
			res = res[0][1]
			if res == hz:
				cacc_num = cacc_num + 1
			cacc_total = cacc_total + 1
			for i in range(len(res)):
				if res[i] == hz[i]: acc_num = acc_num + 1
				acc_total = acc_total + 1
			total_res.append(res)
			#print("acc:",acc_num / acc_total)
			#print("complete acc:", cacc_num / cacc_total)

		eval['acc'] = acc_num / acc_total
		eval['complete acc'] = cacc_num / cacc_total
		return total_res, eval 

def usage():
	print("pinyin -a/--algo <algo> -s -i/--ifile <inputfile> -o/--ofile <outputfile>")
	print("       -i,--ifile <inputfile[*.txt]>")
	print("       -o,--ofile <outputfile[*.txt]>")
	print("       -s,--single: in this mode, you don't need to specify in/out file")
	print("       -a,--algo <algo = word2(default)>: hmm1,hmm2,word2")
	print("                  hmm1: 2-gram char based")
	print("                  hmm2: 3-gram char based")
	print("                  word2: 2-gram term based")
	print("")
	print("eg. pinyin --algo hmm2 -i input.txt -o output.txt")
	print("eg. pinyin -a word2 -s")
def cmd():
	try:
		options,args = getopt.getopt(sys.argv[1:],"hsa:i:o:",["help","single","algo","ifile","ofile"])	
		inputfile = ''
		outputfile = ''
		algo = 'word2'
		single_flag = False
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt,arg in options:
		if opt in ("-h","--help"):
			usage()
			sys.exit(2)
		elif opt in ("-i","--ifile"):
			inputfile = arg
		elif opt in ("-o","--ofile"):
			outputfile = arg
		elif opt in ("-a","--algo"):
			algo = arg
		elif opt in ("-s","--single"):
			single_flag = True
	print("-----opt--------")
	print("inputfile:",inputfile)
	print("output:",outputfile)
	print("algo:",algo)
	print("single_mode:",single_flag)
	if (inputfile == '' or outputfile == '') and not single_flag:
		print("file can't be empty")
		exit(0)
	print("-----opt--------")
	return inputfile,outputfile,algo,single_flag

if __name__ == "__main__":
	inputfile, outputfile, algoname,single_flag = cmd()
	if algoname == 'hmm1':
		algo = viterbi
		param = params.hmm1Params(smooth.Adddelta())
	elif algoname == 'hmm2':
		algo = viterbi2
		param = params.hmm2Params(smooth.Adddelta())
	else:
		algo = dp4word2
		param = params.dagParams() 

	checker = Checker(param,algo)

	if single_flag:
		while True:
			print("input:",end='')
			try:
				text = input()
			except EOFError:
				print("exit")
				break
			text = text.strip().split(' ')
			res = checker.singlepredict(text)
			for i in res:
				print(i)
	else:
		test = open(inputfile[:-3] + '.txt',"r")
		#test = open("./../data/test.pkl","rb")
		exit(0)
		test = pickle.load(test)
		pybatch = [obj[0] for obj in test]
		hzbatch = [obj[1] for obj in test]
		total_res, eval = checker.evaluate(pybatch,hzbatch)

		print(eval)
		print(total_res[:10])