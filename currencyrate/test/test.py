import  sys
sys.path.append("../")

import currency
import dboperate
import time
import random
import graph
currencydict = {0:"CNY", 1:"JPY", 2:"GBP", 3:"CHF",4:"CAD",5:"HKD",6:"FIM", 7:"IEP", 8:"LUF",9:"PTE", 10:"IDR",11:"NZD",12:"SUR",13:"KRW",\
		14:"USD", 15:"EUR",16:"DEM", 17:"FRF",18:"AUD", 19:"ATS",20:"BEF", 21:"ITL", 22:"NLG",23:"ESP",24:"MYR",25:"PHP",26:"SGD",\
		27:"THB"}
convertDict = dict(zip(currencydict.values(), currencydict.keys()))
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
def testCurrencyRate(cr):
	cr.getCurrencyRate()
def testCRDB(db, cr):
	db.createDB("testdb_2")
	db.createTable("testtable_2")
	cr.getCurrencyRate()
	db.addCurrencyRate(cr)
	

def produceList():
	num = len(currencydict)
	sign = []
	for i in range(num):
		for j in range(num):
			if i == j:
				continue
			sign.append(currencydict[i] + currencydict[j])	
	return sign

def testBuildGraph(db):
	print "start"
	db.selectDB("testdb_2")
	db.selectTable("CurrencyTable")
	print "db Done"
	sign = produceList()
	for i in sign:
		t = db.getLastestData(i)
		print t
		


if __name__ == "__main__":
	db = dboperate.DB("localhost", "root", "lishuaiyuan")
	#testDB(db)
	"""sign = produceList()
	cr = currency.CurrencyRate(sign[1:600])
	testCRDB(db, cr)
	cr = currency.CurrencyRate(sign[600:])
	testCRDB(db, cr)"""
	#testCurrencyRate(cr)	
	#print cr
	testBuildGraph(db)
	





