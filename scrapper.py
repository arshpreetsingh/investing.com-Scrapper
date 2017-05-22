from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
import decimal
import time
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
import itertools
import requests

url='https://www.investing.com/instruments/HistoricalDataAjax'

data = {
'action':'historical_data',
'curr_id':'1',
'st_date':'01/01/2012',
'end_date':'05/21/2013',
'interval_sec':'Daily'
}

headers = {
'Host': 'www.investing.com',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip,deflate,br',
'Content-Type': 'application/x-www-form-urlencoded',
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'https://www.investing.com/currencies/eur-usd-advanced-chart',
'Content-Length': '124',
'Cookie': 'SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A2%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%221%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A14%3A%22Euro+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Feur-usd%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%223%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A22%3A%22US+Dollar+Japanese+Yen%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fusd-jpy%22%3B%7D%7D%7D%7D; adBlockerNewUserDomains=1494777603; _ga=GA1.2.361180353.1494777643; editionPostpone=1494777986581; __qca=P0-566080298-1494777694081; optimizelyEndUserId=oeu1494777700284r0.7999239353989546; optimizelySegments=%7B%224225444387%22%3A%22ff%22%2C%224226973206%22%3A%22referral%22%2C%224232593061%22%3A%22false%22%2C%225010352657%22%3A%22none%22%7D; optimizelyBuckets=%7B%7D; __gads=ID=0f206ca28c765aad:T=1494777984:S=ALNI_MYTT5tqiAnVE5pUy8-NxELDS2GjeQ; _gid=GA1.2.1297167314.1495357127; ses_id=N3kxcDM8MTkydmxqbz44OjZmMG8wNmJpZ25jYTo%2BZXM5LTc5YTZjJTY5O3VubWJ%2BMDY%2FPjNlYTA9PmJsNGMzZjdnMTEzNjFlMjFsMm9vODI2ZjBuMGZiNmdiY2k6OmVoOT83NWFhY2U2YTtkbjNiZDAiPyMzd2FwPW9iMjR1M3Q3ODFwM2AxZDJmbGFvOTg9NmcwbDAxYmBnZGNpOm9lfTly; gtmFired=OK; PHPSESSID=2s8hu2us3q3kd2fp6ltthjs2h1; StickySession=id.19162714724.014.www.investing.com; billboardCounter_1=2; geoC=IN; nyxDorf=ODwzZ2I1M3ExYzs%2FYC1jaTNiMXQ%2FOWVjYGk%3D; _gat_allSitesTracker=1; _gat=1',
'Connection': 'keep-alive'
}

Base = declarative_base()

class InvestScrapper(object):
	def __init__(self,url,data,headers):
		self.url=url
		self.data=data
		self.headers=headers
		self.price_list=[]
		self.date_list = []
				
	def get_data(self):
		"""fetch data from given URL"""
		response = requests.post(self.url,data=self.data,headers=self.headers)
		soup= BeautifulSoup(response.text, 'html.parser')
		self.soup=soup
		return self.soup

	def parse_price(self):
		"""parses prrce from raw data"""
		data = self.soup.find_all("td")
		for i in data:
			try:
				self.price_list.append(i.attrs['data-real-value'])
			except:
				pass
		return self.price_list
		
	def parse_date(self):
		"""parses dates from raw data"""
		data = self.soup.find_all("td",{"class":"first left bold noWrap"})
		for i in data:
			self.date_list.append(i.text)
		return self.date_list


class OhlcTable(Base):
	"""Creating SQL model for DB"""
	__tablename__='ohlc_table'
	db_id = Column(Integer, primary_key=True)
	date = Column(Integer,nullable=False)
	open_price = Column(Integer,nullable=True)
	high_price = Column(Integer,nullable=True)
	low_price = Column(Integer,nullable=True)
	close_price = Column(Integer,nullable=True)

if __name__=="__main__":
	
	# fetching required data and saving into lists 
	
	s = InvestScrapper(url,data,headers)
	s.get_data()
	price_list= s.parse_price()
	date_list = s.parse_date()
	list_parts=list(itertools.izip_longest(*[iter(price_list)]*5))
	date_list = [str(x) for x in date_list]
	
	# creating DB engine and session(reuseable) to make bulk Entries
	engine = create_engine('sqlite:///mydb4')
	Base.metadata.create_all(engine)
	session_factory = sessionmaker(bind=engine)
	session = session_factory()
	
	for date,part in zip(date_list,list_parts):
		session.add(OhlcTable(date=date,open_price=part[1],high_price=part[2],low_price=part[3],close_price=part[4]))
#closing DB session
session.commit()
