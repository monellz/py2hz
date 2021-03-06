import math
from dag import DAG,Vertex,Vpool
from interface import encode


def viterbi(params,obs):
	'''
		viterbi algorithms
		obs: pinyin list (input)
	'''
	V = [{}]
	
	cur_states = params.get_states(obs[0])
	#we only need to care about the states(hanzi) corresoponding to cur pinyin
	#instead of the whole wordset	

	#initialize t = 0
	for s in cur_states:
		_prob = math.log(params.start(obs[0],s)) + math.log(params.emit(obs[0],s))
		_path = s 		
		V[0][s] = (_prob,_path)
	
	#run viterbi for t > 0
	for t in range(1, len(obs)):
		V.append({})
		prev_states = cur_states
		cur_states = params.get_states(obs[t])
		for s in cur_states:
			(_prob,_prev_s) = max([(V[t-1][prev_s][0] + math.log(params.trans(prev_s,s)) + math.log(params.emit(obs[t],s)),prev_s) for prev_s in prev_states])
			V[t][s] = (_prob,V[t-1][_prev_s][1] + s) 
	
	#sort the final result
	res = [V[-1][key] for key in V[-1].keys()]
	return sorted(res, key = lambda c: c[0], reverse = True)

		
def _createDAG(params,pool,py_list,cur_v,end):
	'''
		True: cur_v is the end
		False: not end
	'''
	if len(py_list) == 0: return True
	res = params.search_prefix(py_list)
	#print(res)
	for length,hz_list in res.items():
		for hz in hz_list:
			code = encode(hz,py_list[length:])
			v = pool.findVertex(code)
			if v == None:
				v = pool.createVertex(hz,py_list[length:])
				#connect
				cur_v.addnext(v.id)
				v.addprev(cur_v.id)
				#need to expand
				if _createDAG(params,pool,py_list[length:],v,end):
					#connect to the end
					v.addnext(end.id)
					end.addprev(v.id)
			else:
				#connect
				cur_v.addnext(v.id)
				v.addprev(cur_v.id)
				#not need to expand(existed!)
	return False

def createDAG(params,pool,py_list):
	dag = DAG(pool)
	_createDAG(params,pool,py_list,dag.root,dag.end)
	return dag

def dp4word2(params,obs):
	'''2 word model'''
	pool = Vpool()
	DAG = createDAG(params,pool,obs)
	#print("pool len:",len(pool.pool))
	#print("pool keys:",pool.pool.keys())

	res, prob = DAG.maxpath(params)

	'''
	print("show dist")
	for k,v in pool.pool.items():
		print(k,v.word,v.dist)
	'''
	return [(res,prob)]
		
			
def viterbi2(params,obs):
	''' viterbi for 2-order hmm'''
	V = [{}]
	
	cur_states = params.get_states(obs[0])
	#print("t=0")
	#print(cur_states)
	#we only need to care about the states(hanzi) corresoponding to cur pinyin
	#instead of the whole wordset	

	#initialize t = 0
	for s in cur_states:
		_prob = math.log(params.start(obs[0],s)) + math.log(params.emit(obs[0],s))
		_path = s 		
		#print(" t = 0 path:" , s)
		V[0][s] = (_prob,_path)
	#initialize t = 1
	#2-order
	for t in range(1, min(2,len(obs))):
		V.append({})
		prev_states = cur_states
		cur_states = params.get_states(obs[t])
		#print("cur states")
		#print(cur_states)
		for s in cur_states:
			V[t][s] = {}
			for prev_s in prev_states:
				V[t][s][prev_s] = (V[t-1][prev_s][0] + math.log(params.trans(prev_s,s)) + math.log(params.emit(obs[t],s)),V[t-1][prev_s][1] + s)

	#run viterbi for t > 1
	#3-order
	for t in range(2, len(obs)):
		#print("now obs:",obs[t])
		V.append({})
		prev_states = cur_states
		cur_states = params.get_states(obs[t])
		for s in cur_states:
			V[t][s] = {}
			for prev_s in prev_states:
				#(_prob,_preprev_s) = max([(V[t-1][prev_s][preprev_s][0] + math.log(params.trans2(preprev_s,prev_s,s)) + math.log(params.emit2(prev_s,s,obs[t])),preprev_s) for preprev_s in V[t-1][prev_s].keys()])
				(_prob,_preprev_s) = max([(V[t-1][prev_s][preprev_s][0] + math.log(params.trans2(preprev_s,prev_s,s)) + math.log(params.emit(obs[t],s)),preprev_s) for preprev_s in V[t-1][prev_s].keys()])
				V[t][s][prev_s] = (_prob,V[t-1][prev_s][_preprev_s][1] + s) 
	
	#sort the final result
	res = []
	if len(obs) == 1:
		for cur in V[-1].keys():
			res.append(V[-1][cur]) 
	else:
		for cur in V[-1].keys():
			for prev in V[-1][cur].keys():
				res.append(V[-1][cur][prev])

	return sorted(res, key = lambda c: c[0], reverse = True)
