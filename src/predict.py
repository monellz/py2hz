from viterbi import viterbi
from params import hmm1Params



params = hmm1Params()
while True:
	print("input:",end='')
	text = input().strip().split(' ')
	print(text)
	res = viterbi(params,text)
	for i in range(min(len(res),5)):
		print(res[i])
