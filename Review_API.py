from flask import Flask,request,jsonify, send_file,send_from_directory
import os
import pandas as pd

from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/file/<path:path>',methods=['GET'])
def getFile(path):
	#return send_file(path)
	return send_from_directory('images',path)

@app.route('/data/<path:path>',methods=['POST','GET'])
def getExcelFile(path):
	auth = request.args.get('auth')
	if auth == "50HandsOrg":
		return send_file(path)

@app.route('/api')
def api_list():
	return "<center><h1>List of API's</h1></center><br><dl><dt>/</dt><dd>Gets the Yelp response<br>Requires input in the form of JSON with parameter \"location\"<br></dd><dt>/check</dt><dd>To Check API is Online<br></dd><dt>/data</dt><dd>To get URL of US and Canada Data CSV files<br></dd></dl>"

@app.route('/data')
def getData():
	res ={}
	res['us_data'] = request.base_url + '/us_data.csv'
	res['canada_data'] = request.base_url + '/canada_data.csv'
	
	
	return jsonify(res)


@app.route('/status')
def status():
	content = open('status.txt','r').read()
	return content

@app.route('/',methods=['GET','POST'])
def api():
	content = request.json
	loc = content['location']
	
	d1 = pd.read_csv('us_data.csv')
	d2 = pd.read_csv('canada_data.csv')
	data = d1.append(d2)

	check = data['city'] == loc

	result=[]
	for res in data.values:
		temp={}
		temp['name'] = res[15]
		temp['is_closed'] = res[1]
		temp['address'] = res[2]
		temp['overall_rating'] = res[3]

		temp['before_polarity_score'] = res[4]
		temp['before_avg_rating'] = res[5]
		temp['before_sentiment'] = res[6]

		temp['after_polarity_score'] = res[7]
		temp['after_avg_rating'] = res[8]
		temp['after_sentiment'] = res[9]
 
		temp['overall_polarity_score'] = res[10]
		temp['overall_sentiment'] = res[11]

		temp['wordcloud_img_url'] = request.base_url + res[12]
		temp['yelp_url'] = res[14]
		if res[13].lower() == loc.lower():
			result.append(temp)

	print(len(result))
	return jsonify(result)


@app.route('/check')
def check():
	return "API is Online"



if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port="8990")