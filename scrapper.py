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
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
url='https://www.investing.com/currencies/eur-usd-historical-data'
Base = declarative_base()

class InvestScrapper(object):
	def __init__(self,agent,url):
		self.agent=agent
		self.url=url
		self.price_list=[]
		self.date_list = []
				
	def get_data(self):
		"""fetch data from given URL"""
		request = Request(self.url, None, {'User-Agent': self.agent})
		soup= BeautifulSoup(urlopen(request).read(), 'html.parser')
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
	
	s = InvestScrapper(agent,url)
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
	




'''
other_data = soup.find_all("td")
list_parts = []
for i in other_data:
	try:
		list_parts.append(i.attrs['data-real-value'])
	except:
		pass 
list_parts=list(itertools.izip_longest(*[iter(list_parts)]*5))
print list_parts[0][0]

s = scrapper(agent,url)
s.get_data()
#print s.parse_data()
'''
'''
import itertools
other_data = soup.find_all("td")
list_parts = []
for i in other_data:
	try:
		list_parts.append(i.attrs['data-real-value'])
	except:
		pass 
list_parts=list(itertools.izip_longest(*[iter(list_parts)]*5))
print list_parts[0][0]



engine = create_engine('sqlite:////home/metal-machine/Desktop/sqlalchemy_example.db')
metadata= MetaData(engine) 
omdb_data = Table('ohlc_table', metadata,
    Column('ohlc_id', Integer, primary_key=True),
    Column('Date', String(200)),
    Column('Open', Float),
    Column('High', String(200)),
    Column('Low', Float),
    Column('Close', Float),)
omdb_data.create()
mm = omdb_data.insert()


engine = create_engine('sqlite:///mydb2')
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
session = session_factory()

for i in xrange(10):
    session.add(OhlcTable(date=i))

session.commit()

'''
#engine = create_engine('sqlite:////home/metal-machine/Desktop/sqlalchemy_example.db')
#engine = create_engine('sqlite:////home/metal-machine/Desktop/db.sqlite3')
#connection = engine.connect()

#engine = create_engine('sqlite:////home/metal-machine/Desktop/mydb')
#engine = create_engine('sqlite:////home/metal-machine/Desktop/sqlalchemy_example.db')
#connection = engine.connect()
#session_factory = sessionmaker(bind=engine)
#session = session_factory()

#for i in xrange(10):
 #   session.add(m)
#session.commit()

'''

userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
url='https://www.investing.com/currencies/eur-usd-historical-data'
req = Request(url, None, {'User-Agent': userAgent})	
soup = BeautifulSoup(urlopen(req).read(), 'html.parser')

import itertools
other_data = soup.find_all("td")
list_parts = []
for i in other_data:
	try:
		list_parts.append(i.attrs['data-real-value'])
	except:
		pass 
list_parts=list(itertools.izip_longest(*[iter(list_parts)]*5))
print list_parts[0][0]

engine = create_engine('sqlite:////home/metal-machine/Desktop/sqlalchemy_example.db')
metadata= MetaData(engine) 
omdb_data = Table('ohlc_table', metadata,
    Column('ohlc_id', Integer, primary_key=True),
    Column('Date', String(200)),
    Column('Open', Float),
    Column('High', String(200)),
    Column('Low', Float),
    Column('Close', Float),)
omdb_data.create()
mm = omdb_data.insert()

'''
