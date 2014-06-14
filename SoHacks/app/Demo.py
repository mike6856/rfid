from flask import render_template
from app import app
import unirest
from bs4 import BeautifulSoup
import urllib2
import json


@app.route('/')
@app.route('/index')
def home():
	'''response = unirest.get("https://george-vustrey-weather.p.mashape.com/api.php",
	  
	  headers={
	    "X-Mashape-Authorization": "6oqkY2PaGscbxA6261cO3n13mnBH6yxY"
	  },
	  params={
	    "location": "San Antonio"
	  }
	);'''

	googleResponse = unirest.get("https://maps.googleapis.com/maps/api/geocode/json",
	  
	  params={
	    "address": "San Antonio"
	  }
	);
	lat = googleResponse.body['results'][0]['geometry']['location']['lat']
	lng = googleResponse.body['results'][0]['geometry']['location']['lng']

	response = unirest.get("https://simple-weather.p.mashape.com/weatherdata",
	  
	  headers={
	    "X-Mashape-Authorization": "6oqkY2PaGscbxA6261cO3n13mnBH6yxY"
	  },
	  params={
	    "lat": lat,
	    "lng": lng
	  }
	);

	channelSection = response.body['query']['results']['channel']
	conditionString = channelSection['item']['condition']['text']
	bsoup = BeautifulSoup(urllib2.urlopen(channelSection['item']['link']).read())
	imageString = str(bsoup.select('div[class~=yog-bg]')[0].select('img')[0]['src'])
	# if channelSection['units']['temperature'] == 'C'
	# 	windChillC = channelSection['wind']['chill']
	# 	windChillF = windChillC * 9f / 5f + 32
	# 	temperatureC = channelSection['item']['condition']
	# 	temperatureF = temperatureC * 9f / 5f + 32
	# 	temperatureLowC = channelSection['item']['forecast'][0]['low']
	# 	temperatureLowF = temperatureLowC * 9f / 5f + 32
	# 	temperatureHighC = channelSection['item']['forecast'][0]['high']
	# 	temperatureHighF = temperatureHighC * 9f / 5f + 32
	# else
	# 	windChillF = channelSection['wind']['chill']
	# 	windChillC = (windChillF - 32) * 5f / 9f
	# 	temperatureF = channelSection['item']['condition']
	# 	temperatureC = (temperatureF - 32) * 5f / 9f
	# 	temperatureLowF = channelSection['item']['forecast'][0]['low']
	# 	temperatureLowC = (temperatureLowF - 32) * 5f / 9f
	# 	temperatureHighF = channelSection['item']['forecast'][0]['high']
	# 	temperatureHighC = (temperatureHighF - 32) * 5f / 9f
	# if channelSection['units']['distance'] == 'km'
	# 	visibilityKm = channelSection['atmosphere']['visibility']
	# 	visibilityMi = visibilityKm * 0.621371
	# else
	# 	visibilityMi = channelSection['atmosphere']['visibility']
	# 	visibilityKm = visibilityMi * 1.60934
	# humidity = str(channelSection['atmosphere']['humidity']) + '%'
	# sunrise = channelSection['astronomy']['sunrise']
	# sunset = channelSection['astronomy']['sunset']
	# windChillK = windChillC + 273
	# temperatureK = temperatureC + 273
	# temperatureLowK = temperatureLowC + 273
	# temperatureHighK = temperatureHighC + 273
	return render_template("index.html", condition=conditionString, image=imageString)

@app.route('/record')
def record():
	file_in = open("C:\\Users\\LegalPRO\\Desktop\\SoHacks\\app\\test.txt",'r')
	tableData = json.loads(file_in)
	print tableData
	return render_template("recordTable.html", tableData=tableData)