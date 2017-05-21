from math import pi
import pandas as pd
from bokeh.sampledata.stocks import MSFT
from bokeh.plotting import figure, show, output_file
import sqlite3
import pandas as pd
# Create your connection.
'/home/metal-machine/Desktop/mydb4'

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair,zoom_out,\
xzoom_out,yzoom_out,redo,undo,wheel_zoom,xwheel_zoom, ywheel_zoom"

class CreateUI(object):
	
	def __init__(self):
		pass
		#self.output_file=output_file
		#self.chart_title=chart_title
		#self.chart_tools=chart_tools
		#self.plot_width=plot_width
		#self.plot_text=plot_text
	def connecet_db(self,sql_string):
		cnx = sqlite3.connect(sql_string)
		self.cnx=cnx
		return self.cnx
		
	def plot_data(self,db_query,out_file,ui_tools,title):
		df = pd.read_sql_query(db_query,self.cnx)
		df["date"] = pd.to_datetime(df["date"])
		mids = (df.open_price + df.close_price)/2
		spans = abs(df.close_price-df.open_price)
		inc = df.close_price > df.open_price #booleans for Open and Close difference
		dec = df.open_price > df.close_price
		w = 12*60*60*1000 #  passing statically for now
		output_file(out_file, title="example")	    
		p = figure(x_axis_type="datetime", tools=ui_tools, plot_width=1000, toolbar_location="right")
		p.segment(df.date, df.high_price, df.date, df.low_price, color="black")
		p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
		p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")
		p.title = title
		p.xaxis.major_label_orientation = pi/4
		p.grid.grid_line_alpha=0.3
		return show(p)


db_query="SELECT * FROM ohlc_table"
ui_tools = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair,zoom_out,\
xzoom_out,yzoom_out,redo,undo,wheel_zoom,xwheel_zoom, ywheel_zoom"

out_file='hello.html'

title='OHLC'
ui=CreateUI()
ui.connecet_db('/home/metal-machine/Desktop/mydb4')
ui.plot_data(db_query,out_file,ui_tools,title)
