import math


def viterbi(params,obs):
	'''
		viterbi algorithms
		obs: pinyin list (input)
	'''
	V = [{}]
	
	cur_states = params.get_states(obs[0])
	#we only need to care about the states(hanzi) corresoponding to cur pinyin
	#instead of the whold wordset	

	#initialize t = 0
	for s in cur_states:
		_prob = math.log(params.start(obs[0],s)) + math.log(params.emit(obs[0],s))
		_path = s 		
		V[0][s] = (_prob,_path)
	
	#run viterbi for t > 0
	for t in range(1, len(obs)):
		print("now obs:",obs[t])
		V.append({})
		prev_states = cur_states
		cur_states = params.get_states(obs[t])
		for s in cur_states:
			(_prob,_prev_s) = max([(V[t-1][prev_s][0] + math.log(params.trans(prev_s,s)) + math.log(params.emit(obs[t],s)),prev_s) for prev_s in prev_states])
			V[t][s] = (_prob,V[t-1][_prev_s][1] + s) 
	
	#sort the final result
	res = [V[-1][key] for key in V[-1].keys()]
	return sorted(res, key = lambda c: c[0], reverse = True)

			
