import MySQLdb
import time

class DB(object):
	def __init__(self, hostpara, userpara, passwdpara):
		self.cnt = MySQLdb.connect(host = hostpara, user = userpara, passwd = passwdpara)
		self.cur = self.cnt.cursor()
	def createDB(self, name):
		self.cur.execute("create database if not exists %s" % name)
		self.cnt.select_db(name)
	def createTable(self, name):
		self.cur.execute("create table if not exists %s(currency varchar(8) not null, cdate date not null, ctime time not null, currencyrate double default 0.0, bidprice double default 0.0, askprice double default 0.0)" % name)
		self.table = name
	def insertInto(self, li):
		s = "insert into %s values" % self.table;
		self.cur.execute(s + "(%s, %s, %s, %s, %s, %s)", li)
	def updateDB(self):
		self.cnt.commit()
	def closeDB(self):
		self.cur.close()
		self.cnt.commit()
		self.cnt.close()
	def addCurrencyRate(self, cr):
		rownum = cr.size()
		for i in range(rownum):
			currency = cr.sign[i]
			currencyrate = cr.currencyrate[i]
			cdate = cr.date[i]
			ctime = cr.time[i]
			bidprice = cr.bidprice[i]
			askprice = cr.askprice[i]
			li = [currency, cdate, ctime, currencyrate, bidprice, askprice]
			self.insertInto(li)	 
		self.updateDB()






