import urllib2
import urllib
url = r"http://download.finance.yahoo.com/d/quotes.csv"
url2 = r"http://download.finance.yahoo.com/d/quotes.csv?s=USDCNY=X&f=sl1d1t1ba&e=.csv"
class CurrencyRate(object):
	def __init__(self, sign):
		self.sign = sign
		self.currencyrate = []
		self.bidprice = []
		self.askprice = []
	def getCurrencyRate(self):
		spara = str()
		for s in self.sign:
			spara += r"%s=X,"%s
		value = {"s": spara, "f":"sl1d1t1ba", "e":".csv"}
		para = urllib.urlencode(value)
		turl = url + "?" + para
		response = urllib2.urlopen(turl)
		resStr = response.read().strip()
		print resStr
		lines = resStr.split("\n")
		for line in lines:
			li = line.strip().split(",")
			self.currencyrate.append(float(li[1]))
			self.bidprice.append(float(li[4]))
			self.askprice.append(float(li[5]))
	def __str__(self):
		ret = str()
		size = len(self.sign)
		for i in range(size):
			ret +="%s: currency: %s, bidprice: %s, askprice: %s\n"% (self.sign[i], self.currencyrate[i], self.bidprice[i], self.askprice[i])
		return ret

if __name__ == "__main__":
	test = CurrencyRate(["USDCNY", "CNYUSD"])
	test.getCurrencyRate()
	print test
	








