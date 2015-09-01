import urllib2
import urllib
url = r"http://download.finance.yahoo.com/d/quotes.csv"
url2 = r"http://download.finance.yahoo.com/d/quotes.csv?s=USDCNY=X&f=sl1d1t1ba&e=.csv"
class CurrencyRate(object):
	def __init__(self, sign):
		self.sign = sign
		self.date = []
		self.time = []
		self.currencyrate = []
		self.bidprice = []
		self.askprice = []
	def size(self):
		return len(self.time)
	def timeConvert(self, time):#10:23am -> 10:23:00
		if time == "0":
			return time
		time = time[1:-1]
		li = time.split(":")
		hour = int(li[0])
		minute = int(li[1][0:-2])
		if time[-2] == 'p':
			hour += 12
		return "%s:%s:00"%(hour, minute)
	def dateConvert(self, date):#8/29/2015 -> 2015-8-29
		if date == "0":
			return date
		dli = date[1:-1].split("/")
		print "dli: ",dli
		month = int(dli[0])
		day = int(dli[1])
		year = int(dli[2])
		return "%d-%02d-%02d" % (year, month, day)
	def getCurrencyRate(self):
		spara = str()
		for s in self.sign:
			spara += r"%s=X,"%s
		value = {"s": spara, "f":"sl1d1t1ba", "e":".csv"}
		para = urllib.urlencode(value)
		turl = url + "?" + para
		response = urllib2.urlopen(turl)
		resStr = response.read().strip()
		#print resStr
		lines = resStr.split("\n")
		for line in lines:
			if "N/A" in line:
				#continue
				line = line.replace("N/A", "0")
			li = line.strip().split(",")
			self.currencyrate.append(float(li[1]))
			self.date.append(self.dateConvert(li[2]))
			self.time.append(self.timeConvert(li[3]))
			self.bidprice.append(float(li[4]))
			self.askprice.append(float(li[5]))
	def __str__(self):
		ret = str()
		size = len(self.sign)
		for i in range(size):
			ret +="%s: date: %s, time: %s, currency: %s, bidprice: %s, askprice: %s\n"% (self.sign[i], self.date[i], self.time[i], self.currencyrate[i], self.bidprice[i], self.askprice[i])
		return ret

if __name__ == "__main__":
	test = CurrencyRate(["USDCNY", "CNYUSD"])
	test.getCurrencyRate()
	print test
