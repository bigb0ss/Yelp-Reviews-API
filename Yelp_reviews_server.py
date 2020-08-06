from Reviews import *
import time
from datetime import datetime
from tqdm import trange
import sys
import schedule

import time

def yelpReviewsJob():

	try:
		os.listdir('images')
	except:
		os.system('mkdir images')
	finally:
		pass
	usa_cities = open('USA_cities.txt','r').read().split('\n')
	canada_cities = open('Canada_cities.txt','r').read().split('\n')
	print("Started Job")
	file= open('status.txt','w')
	print("<BR> Started on "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><hr>",file=file)
	print("Starting Extraction for USA Cities<br>",file=file)
	print("<br>",file=file)
	file.close()
	for index in trange(len(usa_cities)):
		flag=True
		if flag:
			try:
				x=time.time()
				getYelpData(usa_cities[index],'us')
				y=time.time()
				file = open('status.txt','a')
				print("<br> "+str(index+1)+". Completed request for  : "+usa_cities[index]+"   Time taken : "+str((y-x)/60)+" minutes",file=file)
				#wait for 3 minutes before next request
				flag=False
				time.sleep(15)
			except:
				pass
	file.close()
	file = open('status.txt','a')
	print("<br><br>Completed Extraction for USA Cities<br>",file=file)

	print("<br><hr><br>Started Extraction for Canada Cities<br>",file=file)
	print("<br>",file=file)
	file.close()
	
	for index in trange(len(canada_cities)):
		flag = True
		if flag:
			try:
				x=time.time()
				getYelpData(canada_cities[index],'canada')
				y=time.time()
				file = open('status.txt','a')
				print("<br>"+str(index+1)+". Completed request for  : "+canada_cities[index]+"    Time taken : "+str((y-x)/60)+" minutes",file=file)
				file.close()
				#wait for 3 minutes before next request
				flag=False
				time.sleep(15)
			except:
				pass

	
	file = open('status.txt','a')
	print("<br>",file=file)
	print("<br><br>Completed  Extraction for Canada Cities<br><hr>",file=file)

	print("<BR> Completed on "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z"),file=file)
	file.close()
	print("Completed Job")


schedule.every().wednesday.at("07:10").do(yelpReviewsJob)

while True:
	schedule.run_pending()
	time.sleep(1)
