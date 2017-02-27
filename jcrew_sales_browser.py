from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from bs4 import BeautifulSoup
import urllib2
import numpy as np
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in("samhwangg", "EWiWKDPlRxvS2RgAd8YG")

# test connection
def connectSQL():
	db_config = read_db_config()

	try:
		print('Connecting to MySQL database...')
		conn = MySQLConnection(**db_config)

		if conn.is_connected():
			print('Connection established.')
		else:
			print('Connection failed.')

	except Error as error:
		print(error)

	finally:
		conn.close()
		print('Connection closed.')

# scrape total pages to ensure all pages are searched 
def totalPages():
	url = "https://factory.jcrew.com/search2/index.jsp?N=217+16&Ntrm=&Nsrt=3&Npge=1"

	#opens URL with urllib2 
	exampleFile = urllib2.urlopen(url)
	#stores HTML text in here
	exampleHtml = exampleFile.read()
	#closes the opening of the readin of website
	exampleFile.close()

	#creates BeautifulSoup object to store HTML
	soup = BeautifulSoup(exampleHtml, "html.parser")

	pagination = soup.find("span", {"class": "pagination-total"})

	
	for link in pagination:
		return int(link)

# create new table for daily information
def createNewTable(tableName):
	try:	
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()

		query = "CREATE TABLE " + tableName + "(Name VARCHAR(50) NOT NULL PRIMARY KEY, date_entered TIMESTAMP, Original_Price numeric(6,2) NOT NULL, Discount_Price numeric(6,2) NOT NULL);"

		cursor.execute(query)

		conn.commit

	except Error as e:
		print('Error', e)

	finally:
		cursor.close()
		conn.close()

# iterates through all pages on the website and calls insertInfo to push all information into mySQL 
def connectJcrew():

	tableName = raw_input('Input table name: ')

	#create new table before importing information
	createNewTable(tableName)

	for i in range(totalPages()):
		url = "https://factory.jcrew.com/search2/index.jsp?N=217+16&Ntrm=&Nsrt=3&Npge=" + str(i+1)

		#opens URL with urllib2 
		exampleFile = urllib2.urlopen(url)
		#stores HTML text in here
		exampleHtml = exampleFile.read()
		#closes the opening of the readin of website
		exampleFile.close()

		#creates BeautifulSoup object to store HTML
		soup = BeautifulSoup(exampleHtml, "html.parser")

		#name and prices are stored in figcaptions
		figCaption = soup.find_all("figcaption")
		
		for link in figCaption:
			name = link.contents[1].find_all("a")[0].text
			ogPrice = link.contents[3].find_all("span", {"class": "product-list-price-striked notranslate"})[0].text.replace('$', '')
			disPrice = link.contents[5].find_all("span", {"class": "product-sale-price"})[0].text.replace('$', '')
			insertInfo(tableName, name, ogPrice, disPrice)

# inserts all data into mySQL 
def insertInfo(tableName, name, ogPrice, disPrice):

	query = "INSERT INTO  " + tableName + "(Name, date_entered, Original_Price, Discount_Price)" \
			"VALUES(%s,NOW(),%s,%s)"

	args = (name, ogPrice, disPrice)

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()

		cursor.execute(query, args)

		conn.commit()

	except Error as e:
		print('Error', e)

	finally:
		cursor.close()
		conn.close()

# utilizes plot.ly API to collect all data from SQL and graph it online at plot.ly
def graphPlotly():
	db_config = read_db_config()

	try:
		conn = MySQLConnection(**db_config)
		cursor = conn.cursor()

		tableName = raw_input('Input table name: ')

		command = "SELECT Name, Original_Price, Discount_Price from " + tableName + ";"

		cursor.execute(command)
		rows = cursor.fetchall()

		df = pd.DataFrame( [[ij for ij in i] for i in rows] )
		df.rename(columns={0: 'Name', 1: 'Original_Price', 2: 'Discount_Price'}, inplace=True)
		df = df.sort_values(['Original_Price'], ascending=[1])

		clothing_names = df['Name'] 
		for i in range(len(clothing_names)):
		    try:
		        clothing_names[i] = str(clothing_names[i]).decode('utf-8')
		    except:
		        clothing_names[i] = 'Clothing name decode error'

		trace1 = Scatter(
	    x=df['Discount_Price'],
	    y=df['Original_Price'],
	   	text=clothing_names,
	    mode='markers'
	    )

		layout = Layout(
	    xaxis=XAxis( title='Discount Price' ),
	    yaxis=YAxis( type='log', title='Original Price' )
	    )
	
		data = Data([trace1])
		fig = Figure(data=data, layout=layout)
		py.iplot(fig, filename='Original Price vs. Discount Price')


	except Error as e:
		print(e)

	finally:
		cursor.close()
		conn.close()

def main():
	#connectSQL()
	connectJcrew()
	graphPlotly()

if __name__ == '__main__':
	main()



