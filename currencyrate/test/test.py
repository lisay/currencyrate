import  sys
sys.path.append("../")
import math
import currency
import dboperate
import time
import random
import graph
from head import currencydict
convertDict = dict(zip(currencydict.values(), currencydict.keys()))

#test python database operation
def testDB(db):
	db.createDB("testdb_1")
	db.createTable("testtable_1")	
	currency = "CNYUSD"
	for i in range(100):
		t = time.localtime()
		cdate = "%s-%s-%s"%(t.tm_year, t.tm_mon, t.tm_mday)
		ctime = "%s:%s:%s"%(t.tm_hour, t.tm_min, t.tm_sec)
		currencyrate = random.random()
		bidprice = random.random()
		askprice = random.random()
		li = [currency, cdate, ctime, currencyrate, bidprice, askprice]
		db.insertInto(li)
	db.closeDB()
#test fetch the currancyrate from the url
def testCurrencyRate(cr):
	cr.getCurrencyRate()

#test save the currencyrate fetching from the url to the database 
def testCRDB(db, cr):
	db.createDB("testdb_2")
	db.selectDB("testdb_2")
	db.selectTable("currencytable")
	db.createTable("currencytable")
	cr.getCurrencyRate()
	db.addCurrencyRate(cr)
#test the Priority Queue operation
def testPriorityQueue():
	test  = graph.PriorityQueue()
	test.insert((0, 'p'))
	test.insert((2, 'y'))
	test.insert((3, 'w'))
	test.insert((4, 'e'))
	test.insert((5, 't'))
	test.insert((6, 'r'))
	print test.keys
	print test.dic
	while not test.isEmpty():
		print test.deleteMin()
#return a list containing the currency sign(CNYUSD)
def produceList():
	num = len(currencydict)
	sign = []
	for i in range(num):
		for j in range(num):
			if i == j:
				continue
			sign.append(currencydict[i] + currencydict[j])	
	return sign
#return a graph containing four vertex and a cycle
def produceGraph():
	g = graph.EdgeWeightedDigraph(4)
	d1 = graph.DirectedEdge(0, 1, 1)	 
	d2 = graph.DirectedEdge(1, 2, -2)	 
	d3 = graph.DirectedEdge(2, 0, -3)	 
	d4 = graph.DirectedEdge(2, 3, 1)	 
	dli = [d1,d2,d3,d4]
	for d in dli:
		g.addEdge(d)
	return g
#test the bellman-ford
def testBellmanFord(g):
	bellmanford = graph.BellmanFordSP(g, 0)
	path = bellmanford.pathTo(3)

#test the class to find the cycle in the graph
def testEdgeWeightedCycleFinder(g):
	cyclefinder = graph.EdgeWeightedCycleFinder(g)
#use the data fetching from the url to build a graph
def testBuildGraph(db):
	db.selectDB("testdb_2")
	db.selectTable("currencytable")
	sign = db.getCurrencyList()
	graphpara = graph.EdgeWeightedDigraph(len(currencydict))
	for s in sign:
		v = convertDict.get(s[0:3])
		w = convertDict.get(s[3:])
		c = db.getLastestData(s)
		print v, w
		weight = (-1 * round(math.log(c[0]), 5))
		e = graph.DirectedEdge(v, w, weight)
		graphpara.addEdge(e)
	"""for i in range(graphpara.V()):
		print currencydict[i], ":",
		for e in graphpara.adj(i):
			print e,
		print 	
	"""
	bellmanford = graph.BellmanFordSP(graphpara, 0)
	ret = bellmanford.negativecycle
	#path = bellmanford.pathTo(1)
def produceG(vnum, eli):
	g = graph.EdgeWeightedDigraph(vnum)
	for e in eli:
		g.addEdge(e)
	return g

def testDFOrder(g):
	df = graph.DFOrder(g)
	print df.reverseList()
def runTestDFOrder():
	eli = []
	weight = 1
	eli.append(graph.DirectedEdge(0, 1, weight))
	eli.append(graph.DirectedEdge(0, 2, weight))
	eli.append(graph.DirectedEdge(0, 3, weight))
	eli.append(graph.DirectedEdge(1, 3, weight))
	eli.append(graph.DirectedEdge(2, 4, weight))
	eli.append(graph.DirectedEdge(3, 5, weight))
	eli.append(graph.DirectedEdge(4, 5, weight))
	g = produceG(6, eli)
	testDFOrder(g)

def testTopologyOrder(g):
	t = graph.TopologyOrder(g)
	print t.order()

def runtestTopologyOrder():
	eli = []
	weight = 1
	eli.append(graph.DirectedEdge(0, 1, weight))
	eli.append(graph.DirectedEdge(0, 2, weight))
	eli.append(graph.DirectedEdge(0, 3, weight))
	eli.append(graph.DirectedEdge(1, 3, weight))
	eli.append(graph.DirectedEdge(2, 4, weight))
	eli.append(graph.DirectedEdge(3, 5, weight))
	eli.append(graph.DirectedEdge(4, 5, weight))
	g = produceG(6, eli)
	#g = produceGraph()
	testTopologyOrder(g)
def produceEdgeList(tpl):
	eli = []
	for t in tpl:
		eli.append(graph.DirectedEdge(t[0], t[1], t[2]))
	return eli

def testAcyclicSP(g, s, t):
	print "%s->%s" % (s, t)
	a = graph.AcyclicSP(g, s)
	path = a.pathTo(t)
	if path == None:
		print "No Way"
		return
	for p in path:
		print p
	print a.distTof(t)
def runtestAcyclicSP():
	tpl = [(5, 1, 0.11), (5, 7, 0.12), (5, 4, 0.13) ,(1, 3, 0.21), (3, 7, 0.22), (3, 6, 0.24), (7, 2, 0.33), (0, 2, 0.26),(4, 7, 0.14), (4, 0, 0.15),\
 (6, 2, 0.19), (6, 0, 0.17), (6, 4, 0.33)]
	eli = produceEdgeList(tpl)
	g = produceG(8, eli)
	testAcyclicSP(g, 5, 6)
	print "-"*30
	testAcyclicSP(g, 0, 6)
	print "-"*30
	testAcyclicSP(g, 4, 7)
	print "-"*30
	testAcyclicSP(g, 1, 3)
	print "-"*30
	testAcyclicSP(g, 3, 4)
	print "-"*30
	testAcyclicSP(g, 2, 6)
	print "-"*30
if __name__ == "__main__":
	db = dboperate.DB("localhost", "root", "lishuaiyuan")
	#testDB(db)
	#sign = produceList()
	#cr = currency.CurrencyRate(sign)
	#testCRDB(db, cr)
	#cr = currency.CurrencyRate(sign[600:])
	#testCRDB(db, cr)
	#testCurrencyRate(cr)	
	#print cr
	#g = produceGraph()
	#testBellmanFord(g)
	#testBuildGraph(db)	
	#testEdgeWeightedCycleFinder(g)
	#runTestDFOrder()
	#runtestTopologyOrder()
	runtestAcyclicSP()




