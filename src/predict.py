from viterbi import viterbi, viterbi2
import params 



hmm1p = params.hmm1Params()
hmm2p = params.hmm2Params()
print(type(hmm2p))

while True:
	print("input:",end='')
	text = input().strip().split(' ')
	print(text)
	#res = viterbi(hmm1p,text)
	res = viterbi2(hmm2p,text)
	for i in range(min(len(res),5)):
		print(res[i])
