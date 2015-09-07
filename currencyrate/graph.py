from head import currencydict
class DirectedEdge(object):
	"""directed edge operations"""
	def __init__(self, v, w, weight):
		self.v = v
		self.w = w
		self.weight = weight
	def fromv(self):
		return self.v
	def to(self):
		return self.w
	def __str__(self):
		#return "%s->%s: %s\n" % (currencydict[self.v], currencydict[self.w], self.weight)
		return "%s->%s: %s\n" % (self.v, self.w, self.weight)


class EdgeWeightedDigraph(object):
	"""directed graph with weight, and the adj list is consist of directed edges"""
	def __init__(self, n):
		self.adjpara = list()
		for i in range(n):
			self.adjpara.append(list())#adj list
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
			ret += currencydict[index] + ": \n"
			for e in v:
				ret += str(e)
			ret += "\n"
			index += 1	
		return ret
class PriorityQueue(object):
	"""priority queueu, data structure is bases on a dict and a list, and the key is the priority factor same to the list, and the value is the number of vertex """
	def __init__(self, dic = dict()):
		self.dic = dic
		self.keys = sorted(dic.keys())
	#binary search, and return the pos to insert into
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
	#t is a tuple, t[0] is the number of vertex, t[1] is the distTo[t[0]]				
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
	def __str__(self):
		ret = str()
		for k in self.keys:
			ret += " (%s:%s) " % (k, self.dic[k])
		return ret
	
		
class EdgeWeightedCycleFinder(object):
	"""find the cycle in the graph"""
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
					tcycle.append(self.edgeTo[tv])
					tv = self.edgeTo[tv].fromv()	
				tcycle.append(e)
				self.cycle.append(tcycle)
		self.onstack[v] = False
	def getcycle(self):
		return self.cycle
	def hasCycle(self):
		return len(self.cycle) != 0
class BellmanFordSP(object):
	"""bellman-ford operations"""
	def __init__(self, graphpara, s):
		self.graphpara = graphpara
		self.distTo = list()
		self.edgeTo = list()
		self.negativecycle = list()
		self.hasnegativecycle = False
		self.queue = PriorityQueue()
		self.inqueue = list()
		self.cost = 0
		for i in range(graphpara.vnum):
			self.distTo.append(float("inf"))
			self.edgeTo.append(None)
			self.inqueue.append(False)
		self.s = s
		self.distTo[s] = 0
		self.edgeTo[s] = None
		self.queue.insert((s, 0.0))
		self.inqueue[s] = True
		while (not self.queue.isEmpty()) and (not self.hasNegativeCycle()):
			print "queue: ", self.queue
			index = self.queue.deleteMin()
			print "index: " ,index
			self.inqueue[index] = False
			self.relax(index)
		print "negativeCycle: "
		for n in self.negativecycle:
			for i in n:
				print i,
			print 
		print "queue: ", self.queue
	#relax a vertex
	def relax(self, vpara):
		for e in self.graphpara.adj(vpara):
			v = e.fromv()
			w = e.to()
			if self.distTo[w] > self.distTo[v] + e.weight:
				self.distTo[w] = self.distTo[v] + e.weight
				self.edgeTo[w] = e
				if not self.inqueue[w]:
					self.queue.insert((w, self.distTo[w]))
					self.inqueue[w] = True
			self.cost += 1
			if self.cost % self.graphpara.vnum == 0 and self.cost / self.graphpara.vnum == self.graphpara.vnum:
				self.negativecycle = self.findNegativeCircle()
	#find the nagative cycle
	def findNegativeCircle(self):
		g = EdgeWeightedDigraph(self.graphpara.vnum)
		for e in self.edgeTo:
			if not e == None:
				g.addEdge(e)
		cycleFinder = EdgeWeightedCycleFinder(g)
		cycle = cycleFinder.getcycle()
		return cycle
	def pathTo(self, v):
		path = list()
		tv = v
		count = 0
		while tv != self.s and count < 30:
			count += 1
			path.append(self.edgeTo[tv])
			tv = self.edgeTo[tv].fromv()
		return path
	def hasNegativeCycle(self):
		return len(self.negativecycle) > 0
class DFOrder(object):
	"""traverse graph by depth first order"""
	def __init__(self, G):
		self.G = G
		self.reverseli = []
		self.marked = []
		vnum = G.V()
		for i in range(vnum):
			self.marked.append(False)
		for i in range(vnum):
			if not self.marked[i]:
				self.marked[i] = True
				self.dfs(i)
		self.reverseli.reverse()#reverse the list, to get the topology order
	def dfs(self, v):
		for e in self.G.adj(v):
			vx = e.fromv()
			wx = e.to()
			if not self.marked[wx]:
				self.marked[wx] = True
				self.dfs(wx)
		self.reverseli.append(v)
	def reverseList(self):
		return self.reverseli


class TopologyOrder(object):
	"""acquire the topology order of the acyclic graph"""
	def __init__(self, G):
		cyclefinder = EdgeWeightedCycleFinder(G)	
		df = DFOrder(G)
		self.topologyli = []
		if not cyclefinder.hasCycle():	
			self.topologyli = df.reverseList()
		
	def order(self):
		return self.topologyli

class AcyclicSP(object):
	"""get the shortest path of the acyclic graph"""
	def __init__(self, G, s):
		self.G = G
		self.edgeTo = []
		self.distTo = []
		self.marked = []
		self.vnum = G.V()
		self.s = s
		for i in range(self.vnum):
			self.distTo.append(float("inf"))
			self.edgeTo.append(None)
			self.marked.append(False)
		self.distTo[s] = 0
		topologyorder = TopologyOrder(G)
		order = topologyorder.order()
		for v in order:
			self.relax(v)
	def pathTo(self, v):
		retpath = []
		tv = v
		if not self.hasPathTo(v):
			return
		while tv != self.s:
			e = self.edgeTo[tv]
			retpath.append(e)
			tv = e.fromv()
		return retpath
	def hasPathTo(self, v):
		return self.distTo[v] != float("inf")
	def distTof(self, v):
		return self.distTo[v]
	def relax(self, v):
		for e in self.G.adj(v):
			self.relaxEdge(e)
	def relaxEdge(self, e):
		vx = e.fromv()
		wx = e.to()
		if self.distTo[wx] > self.distTo[vx] + e.weight:
			self.distTo[wx] = self.distTo[vx] + e.weight	
			self.edgeTo[wx] = e

















