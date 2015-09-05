import urllib2
import urllib
url = r"http://download.finance.yahoo.com/d/quotes.csv"
class CurrencyRate(object):
"""fetch the real-time currencyrate from the url"""
	def __init__(self, sign):
		#url para, like CNY to USD: CNYUSD
		self.sign = sign
		#date\time\currencyrate\bidprice\askprice are the data return as the repond
		self.date = []
		self.time = []
		self.currencyrate = []
		self.bidprice = []
		self.askprice = []
	def size(self):
		return len(self.time)
	#1:23pm -> 13:23:00
	def timeConvert(self, time):
		if time == "0":
			return time
		time = time[1:-1]
		li = time.split(":")
		hour = int(li[0])
		minute = int(li[1][0:-2])
		if time[-2] == 'p':
			hour += 12
		return "%s:%s:00"%(hour, minute)
	#8/29/2015 -> 2015-8-29
	def dateConvert(self, date):		
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
		lines = resStr.split("\n")
		for line in lines:
			#there is no currencyrate bewteen two currency
			if "N/A" in line:
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
