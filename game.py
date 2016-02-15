import requests 
import time
import urllib2
import numpy
import talib
import re
import datetime

class Game():

	def __init__(self,curr,fastperiod,slowperiod,signalperiod):
		self.curr = curr
		self.last,self.bids, self.asks, = self.open_files()
		self.uptrend = False
		self.downtrend = False
		self.buy_price = 0
		self.short_price = 0
		self.macd = 0
		self.signal = 0
		self.fastperiod = fastperiod
		self.slowperiod= slowperiod
		self.signalperiod = signalperiod
		while True:
			trader.start()
		
	def buy(self):
		print "trade: buy @ ",self.bid
		self.get_tick()
		self.buy_price = self.ask
		#wait till buy price is greater than spread + 1pip

	def short(self):
		print "trade: short @", self.ask
		self.get_tick()
		self.short_price = self.bid
		#wait till short price is greater than spread + 1pip
		while True:
			self.trends()
			if self.uptrend == True:
				self.exit_short()
				break

	def exit_buy(self):
		self.trends()
		print "exit buy @ ",self.ask, " buy price=",self.buy_price

	def exit_short(self):
		self.trends()
		print "exit short @ ", self.bid, " short price=",self.short_price
		self.start()

	def wait_for_uptrend(self):
		print "wait_for_uptrend"
		print self.bid, self.ask, datetime.datetime.utcnow()
		while True:
			self.trends()
			print self.bid, self.ask, datetime.datetime.utcnow()
			if self.uptrend == True:
				self.buy()
				break
			time.sleep(3)

	def wait_for_downtrend(self):
		print "wait_for_downtrend"
		print self.bid, self.ask, datetime.datetime.utcnow()
		while True:
			self.trends()
			print self.bid, self.ask, datetime.datetime.utcnow()
			if self.downtrend == True and self.macd < 0:
				self.short()
				break
			time.sleep(3)

	def start(self):
		print "start"
		#append new tick every x seconds
		while True:
			self.trends()
			if self.uptrend == True:
				self.wait_for_downtrend()
				break
			else:
				self.wait_for_uptrend()
				break
			time.sleep(3)


	def open_files(self):
		last_ticks = []
		bid_ticks = []
		ask_ticks = []

		for i in range(1,12):
			if i < 10:
				LAST = "DAT_NT_NZDUSD_T_LAST_2015" + str(0)+str(i)+str(".csv")
				BID = "DAT_NT_NZDUSD_T_BID_2015"+ str(0)+str(i)+str(".csv")
				ASK = "DAT_NT_NZDUSD_T_ASK_2015" + str(0)+str(i)+str(".csv")
			else:
				LAST = "DAT_NT_NZDUSD_T_LAST_2015" + str(i)+str(".csv")
				BID = "DAT_NT_NZDUSD_T_BID_2015" + str(i)+str(".csv")
				ASK = "DAT_NT_NZDUSD_T_ASK_2015" + str(i)+str(".csv")

			LAST = open(str(LAST))
			BID = open(str(BID))
			ASK = open(str(ASK))
			regex = re.compile("0\..*;")

			for L,B,A in zip(LAST,BID,ASK):

				last_interval = regex.search(L)
				bid_interval = regex.search(B)
				ask_interval = regex.search(A)

				last_interval = last_interval.group(0)
				bid_interval = bid_interval.group(0)
				ask_interval = ask_interval.group(0)

				last_interval = last_interval.replace(';','')
				bid_interval = bid_interval.replace(';','')
				ask_interval = ask_interval.replace(';','')

				last_ticks.append(float(last_interval))
				bid_ticks.append(float(bid_interval))
				ask_ticks.append(float(ask_interval))

		return numpy.array(last_ticks), numpy.array(bid_ticks), numpy.array(ask_ticks)

	def get_tick(self):
		#auth
		param = "http://webrates.truefx.com/rates/connect.html?u=jessekl&p=helloworld&q=ozrates&c="+self.curr+"&s=n"
		x = requests.get(param)
		key = x.content[-15:]
		param = str('http://webrates.truefx.com/rates/connect.html?id=jessekl:helloworld:ozrates:'+key)
		response = urllib2.urlopen(param)
		html = response.read()
		x= html
		self.bid = float(x[7:14])
		self.ask = float(x[14:21])	

	def trends(self):
		self.get_tick()
		numpy.append(self.bids,self.bid)
		numpy.append(self.asks,self.asks)
		m,s,h = talib.MACD(self.bids,fastperiod=self.fastperiod,slowperiod=self.slowperiod,signalperiod=self.signalperiod)
		self.macd = m[-1:]
		self.signal = s[-1:]
		if m.tolist()[-1:] > s.tolist()[-1:]:
			self.uptrend = True
			self.downtrend = False
		else: 
			self.uptrend = False
			self.downtrend = True

		
if __name__ =="__main__":
	#=2400,slow=5200,signal=1800
	#30,60,10
	trader = Game("NZD/USD",fastperiod=7200,slowperiod=14400,signalperiod=2400)



