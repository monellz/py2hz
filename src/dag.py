import math
from interface import encode


class Vertex:
	def __init__(self,word,residue_py_list):
		self.id = encode(word,residue_py_list)
		self.word = word  #hanzi string
		self.residue_py_list = residue_py_list

		self.prev_id_set = set() #set of prev vertex id
		self.next_id_set = set() #set of next vertex id
		self.flag = False
		self.dist = -1e10 #dist from root
		self.father_id = 0 #最优路径上的father id
		'''
		print("initial --vertex")
		print("word:",self.word)
		print("id:",self.id)
		'''
	def reset(self):
		self.flag = False
		self.dist =  -1e10
	def addprev(self,v_id):
		self.prev_id_set.add(v_id)
	def removeprev(self,v_id):
		'''
		print("---remove prev---")
		print("self.id:",self.id)
		print("self.word:",self.word)
		print("prev.set:",self.prev_id_set)
		print("v_id:",v_id)
		print("-----")
		'''
		self.prev_id_set.remove(v_id)
	def addnext(self,v_id):
		self.next_id_set.add(v_id)
	def removenext(self,v_id):
		self.next_id_set.remove(v_id)
		

class Vpool:
	'''pool of vertex'''
	def __init__(self):
		self.num = 0 #number of vertex
		self.pool = {} #dist of all vertex {id:vertex}
		self.none_cnt = 0
	def createVertex(self,word,residue_py_list):
		v = Vertex(word,residue_py_list)
		self.pool[v.id] = v
		return v
	def createNone(self):
		v = Vertex('',[str(self.none_cnt)])	
		self.pool[v.id] = v
		self.none_cnt = self.none_cnt + 1
		return v
	def getVertex(self,v_id):
		return self.pool[v_id]
	def findVertex(self,code):
		if code not in self.pool.keys():
			return None
		else:
			return self.pool[code]

class DAG:
	def __init__(self,pool):
		self.pool = pool
		#store all nodes in this graph
        
		self.root = self.pool.createNone()
		self.end = self.pool.createNone()
		self.stack = []
	def denseconnect(self,dag):
		'''
			g1: root1 -> node1 -> end1
			g2: root2 -> node2 -> end2

			new g: roo1 -> node1 -> node2 -> end2
		'''
		if dag == None: return
		'''
		print("---into dense connect----")
		print("first self.root.id:",self.root.id)
		print("first self.end.id:",self.end.id)
		print("second dag.root.id:",dag.root.id)
		print("second dag.end.id:",dag.end.id)
		'''
		pre = list(self.end.prev_id_set)
		nxt = list(dag.root.next_id_set)
		'''
		print("pre:",pre)
		'''
		for n_id in nxt:
			n = dag.pool.getVertex(n_id)
			n.removeprev(dag.root.id)
		for p_id in pre:
			p = self.pool.getVertex(p_id)
			p.removenext(self.end.id)
			for n_id in nxt:
				n = dag.pool.getVertex(n_id)
				
				#connect
				p.addnext(n.id)
				n.addprev(p.id)
		self.end = dag.end
		#print("----end connect----")
	def parallelconnect(self,dag):
		'''
			g1: root1 -> node1 -> end1
			g2: root2 -> node2 -> end2

			new g: root1 -> node1 -> end1
			             -> node2 ->
		'''
		if dag == None: return
		left = list(dag.root.next_id_set)
		right = list(dag.end.prev_id_set)
		#maybe equal!!
		for l_id in left:
			l = self.pool.getVertex(l_id)
			l.removeprev(dag.root.id)
			l.addprev(self.root.id)
			self.root.addnext(l_id)
		for r_id in right:
			r = self.pool.getVertex(r_id)
			r.removenext(dag.end.id)
			r.addnext(self.end.id)
			self.end.addprev(r_id)

	def __toposort(self,node):
		node.flag = True
		for nxt_id in node.next_id_set:
			nxt = self.pool.getVertex(nxt_id)
			#print("nxt.word:",nxt.word)
			if nxt.flag == False:
				self.__toposort(nxt)
		self.stack.append(node.id)
	def toposort(self):
		'''return a stack'''
		self.stack = []
		#reset flag:  只排序一次
		self.__toposort(self.root)
	def showword(self,v_id):
		v = self.pool.getVertex(v_id)
		return v.word	
	def showprev(self):
		prev = self.root.next_id_set
		for v_id in prev:
			print(self.showword(v_id))
		
	def showstack(self):
		for v in self.stack:
			print(self.showword(v))
	def maxpath(self,params):
		self.toposort()
		self.stack = self.stack[::-1] #reverse
		self.root.dist = 0
		'''
		print("len stack:",len(self.stack))
		print("show----stack")
		self.showstack()
		'''

		for v_id in self.stack:
			v = self.pool.getVertex(v_id)
			'''
			print("cur_v:",v.word)
			print("cur_next:",v.next_id_set)
			'''
			for nxt_id in v.next_id_set:
				nxt = self.pool.getVertex(nxt_id)
				prob = math.log(params.trans(v.word,nxt.word))
				if prob > 0:
					print(prob)
					print(v.word,nxt.word)
				if nxt.dist < v.dist + prob:
					nxt.dist = v.dist + prob
					nxt.father_id = v.id
		res = []
		cur_id = self.end.id

		while cur_id != self.root.id:
			#print(cur_id)
			cur = self.pool.getVertex(cur_id)
			res.append(cur.word)
			#print(cur.word)
			cur_id = cur.father_id
		
		res = res[::-1][:-1]
		return self.end.dist, ''.join(res),
