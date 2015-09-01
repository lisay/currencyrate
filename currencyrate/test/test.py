import  sys
sys.path.append("../")

import currency
import dboperate
import time
import random
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
	
if __name__ == "__main__":
	db = dboperate.DB("localhost", "root", "lishuaiyuan")
	#testDB(db)
	sign = ["CNYJPY", "CNYUSD", "CNYEUR"]
	cr = currency.CurrencyRate(sign)
	testCRDB(db, cr)
	#testCurrencyRate(cr)	
	print cr





