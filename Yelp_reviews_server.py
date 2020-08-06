from Reviews import *
import time
from datetime import datetime

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

	columns=['name','is_closed','address','overall_rating','before_polarity_score','before_avg_rating','before_sentiment','after_polarity_score','after_avg_rating','after_sentiment','overall_polarity_score','overall_sentiment','wordcloud_img_url','city','yelp_url','res_name']
	dummy = pd.DataFrame(columns=columns)

	if not os.path.exists('canada_data.csv'):
		dummy.to_csv('canada_data.csv',index=False)

	if not os.path.exists('us_data.csv'):
		dummy.to_csv('us_data.csv',index=False)


	usa_cities = open('USA_cities.txt','r').read().split('\n')
	canada_cities = open('Canada_cities.txt','r').read().split('\n')
	print("Started Job")
	file= open('status.txt','w')
	print("<BR> Started on "+datetime.now().strftime("%d-%B-%Y  %I:%M %p  %Z")+"<br><hr>",file=file)
	print("Starting Extraction for USA Cities<br>",file=file)
	print("<br>",file=file)
	file.close()
	for index in range(len(usa_cities)):
		flag=True
		if flag:
			try:
				x=time.time()
				getYelpData(usa_cities[index],'us',True)
				y=time.time()
				file = open('status.txt','a')
				print("<br> "+str(index+1)+". Completed request for  : "+usa_cities[index]+"   Time taken : "+str((y-x)/60)+" minutes",file=file)
				file.close()
				
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
	
	for index in range(len(canada_cities)):
		flag = True
		if flag:
			try:
				x=time.time()
				getYelpData(canada_cities[index],'canada')
				y=time.time()
				file = open('status.txt','a')
				print("<br>"+str(index+1)+". Completed request for  : "+canada_cities[index]+"    Time taken : "+str((y-x)/60)+" minutes",file=file)
				file.close()
				
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


schedule.every().thursday.at("20:55").do(yelpReviewsJob)

while True:
	schedule.run_pending()
	time.sleep(1)