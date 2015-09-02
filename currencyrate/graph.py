currencydict = {0:"CNY", 1:"JPY", 2:"GBP", 3:"CHF",4:"CAD",5:"HKD",6:"FIM", 7:"IEP", 8:"LUF",9:"PTE", 10:"IDR",11:"NZD",12:"SUR",13:"KRW",\
		14:"USD", 15:"EUR",16:"DEM", 17:"FRF",18:"AUD", 19:"ATS",20:"BEF", 21:"ITL", 22:"NLG",23:"ESP",24:"MYR",25:"PHP",26:"SGD",\
		27:"THB"}
class DirectedEdge(object):
	def __init__(self, v, w, weight):
		self.v = v
		self.w = w
		self.weight = weight
	def fromv(self):
		return self.v
	def to(self):
		return self.w
	def __str__(self):
		return "%s->%s: %s\n" % (currencydict[self.v], currencydict[self.w], self.weight)


class EdgeWeightedDigraph(object):
	def __init__(self, n):
		self.adjpara = list()
		for i in range(n):
			self.adjpara.append(list())#lin jie biao
		self.vnum = n
		self.enum = 0
	def addEdge(self, e):
		self.adjpara[e.v].append(e)
		self.enum += 1
	def adj(self, v):
		return self.adjpara[v]
	def edges(self):
		ret = list()
		for v in self.adj:
			for e in v:
				ret.append(e)
		return ret
	def V(self):
		return self.vnum
	def E(self):
		return self.enum
	def __str__(self):
		ret = str()
		index = 0
		for v in self.adjpara:
			ret += currencydict[index] + ": "
			for e in v:
				ret += str(e)
			ret += "\n"
			index += 1	
		return ret
class PriorityQueue(object):
	def __init__(self, dic = dict()):
		self.dic = dic
		self.keys = sorted(dic.keys())
	def rank(self, v):
		lo = 0
		hi = len(self.keys) - 1
		while lo <= hi:
			mid = lo + (hi - lo) / 2
			if self.keys[mid] > v:
				hi = mid - 1
			elif self.keys[mid] < v:
				lo = mid + 1
			else:
				return mid
		return lo				
	def insert(self, t):
		self.dic[t[1]] = t[0]
		self.keys.insert(self.rank(t[1]), t[1])#a[1.01] = 0, a[0.789] = 1, ...
	def deleteMin(self):
		if self.isEmpty():
			return None
		else:
			value = self.dic.pop(self.keys[0])
			self.keys.pop(0)
			return value
	def isEmpty(self):
		return len(self.dic) == 0
	
		
class EdgeWeightedCycleFinder(object):
	def __init__(self, graph):
		self.onstack = list()
		self.cycle = list()
		self.marked = list()
		self.edgeTo = list()
		n = graph.vnum
		for i in range(n):
			self.edgeTo.append(float("inf"))
			self.onstack.append(False)
			self.marked.append(False)
		for v in range(n):
			if not self.marked[v]:
				self.dfs(graph, v)
	def dfs(self, G, v):
		self.onstack[v] = True
		self.marked[v] = True
		for e in G.adj(v):
			w = e.to()
			if not self.marked[w]:
				self.edgeTo[w] = e
				self.dfs(G, w)
			elif self.onstack[w]:
				tcycle = list()
				tv = v
				while tv != w:
					tcycle.append(edgeTo[tv])
					tv = edgeTo[tv].fromv()
				self.cycle.append(tcycle)
		self.onstack[v] = False
	def getcycle(self):
		return self.cycle
	def hasNegativeCycle(self):
		return self.cycle.count() == 0
class BellmanFordSP(object):
	def __init__(self, graphpara, s):
		self.graphpara = graphpara
		self.distTo = list()
		self.edgeTo = list()
		self.negativecycle = list()
		self.queue = PriorityQueue()
		self.inqueue = list()
		self.cost = 0
		for i in range(graphpara.vnum):
			self.negativecycle.append(None)
			self.distTo.append(float("inf"))
			self.edgeTo.append(None)
			self.inqueue.append(False)
		self.s = s
		self.distTo[s] = 0
		self.edgeTo[s] = None
		self.queue.insert((s, 0.0))
		self.inqueue[s] = True
		while not self.queue.isEmpty():
			index = self.queue.deleteMin()
			self.inqueue[index] = False
			self.relax(index)
	def relax(self, v):
		for e in self.graphpara.adj(v):
			v = e.fromv()
			w = e.to()
			if self.distTo[w] > self.distTo[v] + e.weight:
				self.distTo[w] = self.distTo[v] + e.weight
				self.edgeTo[w] = e
				if not self.inqueue[w]:
					self.queue.insert((w, self.distTo[w]))
					self.inqueue[w] = True
				self.cost += 1
				if self.cost % self.graphpara.vnum == 0:
					self.negativecycle = self.findNegativeCircle();					
	def findNegativeCircle(self):
		graph = EdgeWeightedDigraph(self.graphpara.vnum)
		for e in self.edgeTo:
			if not e == None:
				graph.addEdge(e)
		cycleFinder = EdgeWeightedCycleFinder(graph)
		cycle = cycleFinder.getcycle()
		return cycle
	def pathTo(self, v):
		path = list()
		tv = v
		while tv != s:
			path.append(edgeTo[tv])
			tv = edgeTo[tv].fromv()
		return path


#if __name__ == "__main__":
	
