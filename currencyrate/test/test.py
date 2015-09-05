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
	testBuildGraph(db)	
	#testEdgeWeightedCycleFinder(g)
	





