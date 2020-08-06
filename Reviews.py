from tqdm import tqdm
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from datetime import datetime
from lxml import html
from wordcloud import WordCloud, STOPWORDS


import pandas as pd
#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


import os
from random import randint

#proxy_server = RequestProxy()
#proxy_list = proxy_server.get_proxy_list()




def generateWordCloud(data,name,location):
	reviews=""
	for i in data:
		reviews = reviews +" "+i[0]

	wordcloud = WordCloud(width = 3000, height = 1000, random_state=1,background_color='salmon', colormap='Pastel1', collocations=False,stopwords = STOPWORDS).generate(reviews)
	img = wordcloud.to_image()
	name = name.replace(" ","")
	img.save("images/"+location+"_"+name+".jpeg", "JPEG", quality=80, optimize=True, progressive=True)

def getSentiment(reviews):
	total_score=0
	analyzer = SentimentIntensityAnalyzer()
	if len(reviews)==0:
		return 0.0
	for text in reviews:
		score =  analyzer.polarity_scores(text)
		total_score+=score['compound']

	total_score/= float(len(reviews))
	return total_score


def getReviewDetails(url,count):
	review_xpath="//ul/li//span[@lang='en']"
	rating_xpath = "//div[@aria-live]//div[contains(@aria-label,'star rating')]"
	date_xpath = "//div[@aria-live]//span[@class='lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-']"
	flag=False
	flag1=False
	p_list = ["118.27.18.60:8081","78.46.113.151:3128","103.216.51.210:8191","219.121.1.93:3128","41.33.242.150:999"]
	proxy_list = ["198.50.177.44:44699","165.225.36.51:10605","1.1.1.19:80","1.0.0.249:80","1.0.0.129:80",]
	index= randint(0,len(proxy_list)-1)
	
	while not flag:
		try:
			s = requests.Session()
			
			if count==0:
				page = requests.get(url)
				flag1=True
			elif count==1:
				s.proxies= {"http":"198.50.177.44:44699","https":"198.50.177.44:44699" }
			elif count==2:
				s.proxies= {"http":"118.27.18.60:8081","https":"118.27.18.60:8081" }
			elif count==3:
				s.proxies= {"http":"1.0.0.89:80","https":"1.0.0.89:80" }
			else:
				s.proxies = {"http":proxy_list[index],"https":proxy_list[index] }
			
			if not flag1:
				page = s.get(url)
			tree = html.fromstring(page.content)

			reviews_text = tree.xpath(review_xpath)
			ratings_text = tree.xpath(rating_xpath)
			date_text = tree.xpath(date_xpath)

			flag=True
		except:
			count+=1
			index1= randint(0,len(proxy_list)-1)
			while index != index1:
				index1= randint(0,len(proxy_list)-1)
			index = index1
			if count ==5:
				count=0


			

	reviews = []
	for text in reviews_text:
		reviews.append(text.text)

	ratings=[]
	for text in ratings_text:
		ratings.append(text.attrib['aria-label'].split()[0])

	
	dates = []
	for text in date_text:
		dates.append(text.text)

	data =[]
	for i in range(len(reviews)):
		data.append([reviews[i],ratings[i],dates[i]])


	return data,count

def splitData(data):
	processed_data=[]
	split_date = datetime.strptime("20/1/2020","%d/%m/%Y")

	before = []
	after = []
	for i in data:
		if split_date.date() <= datetime.strptime(i[2],"%m/%d/%Y").date():
			after.append(i)
		else:
			before.append(i)

	processed_data.append(before)
	processed_data.append(after)
	return processed_data

def ratingAvg(data):
	tot=0
	if len(data) ==0:
		return 0.0
	for i in data:
		tot+= float(i[1])
	avg= tot/len(data)
	return avg


def getYelpData(location,country,limit_flag=False):
	print("Started Requested")

	api_key = "PrRLUuJ_BSOdTuATW8eQWEvrEx8uTPwdSkrmqgogAt6XB48Iby7XmterstsDVvP7Qi66acf0DHFjXcIcuqe7-wrJ9k6BCy9vI-idE6xiN3QsAZluhTeLqOoSOXEOX3Yx"
	header = {'Authorization': ('Bearer '+api_key)}

	res = requests.get("https://api.yelp.com/v3/businesses/search",params={"location":location,"limit":50,"categories":["Restaurants"]},headers=header)
	out = res.json()	

	print("Got Results from Yelp")
	result=[]
	count=0

	tot = len(out['businesses'])
	if limit_flag:
		tot=2

	for i in tqdm(out['businesses'][:tot]):
		temp={}
		temp['name']=i['name'].lower()
		temp['is_closed']=i['is_closed']		
		address=""
		for x in i['location']['display_address']:
			address = address+" "+x
		temp['address'] = address
		temp['overall_rating'] = i['rating']

		data,count = getReviewDetails(i['url'],count)



		data1 = splitData(data)
		bdata = data1[0]
		adata = data1[1]

		# Before Covid Data Processing

		breviews=[]
		for j in bdata:
			breviews.append(j[0])
		score = getSentiment(breviews)
		temp['before_polarity_score']=score
		temp['before_avg_rating'] = ratingAvg(bdata)

		if temp['before_polarity_score'] > 0.5:
			temp['before_sentiment']="Positive"
		elif temp['before_polarity_score'] == 0.5:
			temp['before_sentiment'] = "Neutral"
		else:
			temp['before_sentiment'] = "Negative"


		# After Covid Data Processing


		if len(adata)!=0:
			areviews=[]
			for j in adata:
				areviews.append(j[0])
			score = getSentiment(areviews)
			temp['after_polarity_score']=score

		
			temp['after_avg_rating'] = ratingAvg(adata)


			if temp['after_polarity_score'] > 0.5:
				temp['after_sentiment']="Positive"
			elif temp['after_polarity_score'] == 0.5:
				temp['after_sentiment'] = "Neutral"
			else:
				temp['after_sentiment'] = "Negative"

			rev =[]
			for j in data:
				rev.append(j[0])
			temp['overall_polarity_score'] = getSentiment(rev)

			if temp['overall_polarity_score'] > 0.5:
				temp['overall_sentiment']="Positive"
			elif temp['overall_polarity_score'] == 0.5:
				temp['overall_sentiment'] = "Neutral"
			else:
				temp['overall_sentiment'] = "Negative"
			generateWordCloud(data,i['name'],location)
			temp['wordcloud_img_url'] =  "file/"+location+"_"+temp['name'].replace(" ","")+".jpeg"
			temp['city']=location.lower()
			temp['yelp_url'] = i['url']
			temp['res_name'] = i['name']
			result.append(temp)

	print("Completed Requested")
	dataFrame = pd.DataFrame(result)

	if country.lower()=='us':
		#print("us")
		file_name='us_data.csv'

	if country.lower()=='canada':
		print('canada')
		#file_name ='canada_data.csv'

	
	fileDataFrame = pd.read_csv(file_name)
	for restaurent in result:
		check = fileDataFrame[fileDataFrame['city']==location.lower()]['name']==restaurent['name'].lower()
		num_index = check[check].index
		idx = num_index  #common place index
		if check.any():
			print("Updating Existing Row")
			fileDataFrame.loc[idx,'is_closed'] = restaurent['is_closed']

			fileDataFrame.loc[idx,'before_polarity_score'] = restaurent['before_polarity_score']
			fileDataFrame.loc[idx,'before_avg_rating'] = restaurent['before_avg_rating']
			fileDataFrame.loc[idx,'before_sentiment'] = restaurent['before_sentiment']
			fileDataFrame.loc[idx,'after_polarity_score'] = restaurent['after_polarity_score']
			fileDataFrame.loc[idx,'after_avg_rating'] = restaurent['after_avg_rating']
			fileDataFrame.loc[idx,'after_sentiment'] = restaurent['after_sentiment']
			fileDataFrame.loc[idx,'overall_polarity_score'] = restaurent['overall_polarity_score']
			fileDataFrame.loc[idx,'overall_rating'] = restaurent['overall_rating']
			fileDataFrame.loc[idx,'overall_sentiment'] = restaurent['overall_sentiment']

			fileDataFrame.loc[fileDataFrame[check].index,'wordcloud_img_url'] = restaurent['wordcloud_img_url']

			fileDataFrame.to_csv(file_name,index=False)	#print("Updated the existing values")
		else:
			print("Adding New Row")
			fileDataFrame = fileDataFrame.append(restaurent,ignore_index=True)
			fileDataFrame.to_csv(file_name,index=False)	


	print("completed saving process in excel file")
