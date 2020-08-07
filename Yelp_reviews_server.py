from Reviews import *
import time
from datetime import datetime
from Reviews import prepare
import sys
import schedule

import time


import smtplib, ssl

def mail(subject):
	print(subject)

def yelpReviewsJob():

	prepare()

	file = open('USA_cities.txt','r')
	usa_cities = file.read().split('\n')
	file.close()
	file = open('Canada_cities.txt','r')
	canada_cities = file.read().split('\n')
	file.close()


	print("Started Job")
	file= open('status.txt','w+')
	print("<BR> Started on "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><hr>",file=file)
	print("Starting Extraction for USA Cities<br>",file=file)
	print("<br>",file=file)
	for index in range(len(usa_cities)):
		flag=True
		if flag:
			try:
				print("<BR> Start "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br>",file=file)
				print(usa_cities[index],file=file)
				x=time.time()
				getYelpData(usa_cities[index],'us')
				y=time.time()
				print("<br> "+str(index+1)+". Completed request    Time taken : "+str((y-x)/60)+" minutes",file=file)
				print("<BR> Stop "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><br>",file=file)
				
				flag=False
				time.sleep(15)
			except:
				pass

	time.sleep(15)
	print("<br><br>Completed Extraction for USA Cities<br>",file=file)

	print("<br><hr><br>Started Extraction for Canada Cities<br>",file=file)
	print("<br>",file=file)

	for index in range(len(canada_cities)):
		flag = True
		if flag:
			try:
				print("<BR> Start "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><br>",file=file)
				print(canada_cities[index],file=file)
				x=time.time()
				getYelpData(canada_cities[index],'canada')
				y=time.time()
				print("<br>"+str(index+1)+". Completed request    Time taken : "+str((y-x)/60)+" minutes",file=file)
				print("<BR> Stop "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><br>",file=file)
				
				flag=False
				time.sleep(15)
			except:
				pass

	
	print("<br>",file=file)
	print("<br><br>Completed  Extraction for Canada Cities<br><hr>",file=file)
	print("<BR> Completed on "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z"),file=file)
	file.close()
	print("Completed Job")


schedule.every().friday.at("15:16").do(yelpReviewsJob)

while True:
	schedule.run_pending()
	time.sleep(1)