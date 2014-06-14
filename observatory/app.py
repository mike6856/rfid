from flask import Flask
from flask import render_template
import unirest
from bs4 import BeautifulSoup
import urllib2
import json
from twilio.rest import TwilioRestClient
import datetime
import time

app = Flask(__name__)

@app.route('/auth/<rfid_num>')
def auth(rfid_num):
    #Read Number
    file = open('/root/rfid/observatory/static/users/users.txt', 'r')
    print type(rfid_num)
    clean_rfid = ''
    for i in rfid_num.strip():
        if ord(i) > 47:
            clean_rfid += str(i)
    print clean_rfid
    logarray = []
    logs = open('/root/rfid/observatory/static/users/logs.txt', 'r')
    jsLog = json.load(logs)
    for loog in jsLog:
         logarray.append(loog)
    logs = open('/root/rfid/observatory/static/users/logs.txt', 'w')
    for user in file:
        pw = user.split(' ')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if str(pw[1].strip()) == clean_rfid:
            log = {'name': pw[0], 'time': st}
            logarray.append(log)
            json.dump(logarray,logs)
            return 'Access granted'
    # put your own credentials here
    #ACCOUNT_SID = "AC02097a03880e5b0a1ce530568ccf7d2e"
    #AUTH_TOKEN = "5ee2dff50a471398f740829a886416a6"
    #client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    #client.messages.create(to="(915)256-3811", from_="+19154932791", body="Access denied to front door.", )
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    log = {'name': 'Unknown Denied', 'time': ts}
    logarray.append(log)
    json.dump(logarray,logs)
    return "DENIED"

@app.route('/add/<new_card>')
def add(new_card):
    file = open('/root/rfid/observatory/static/users/users.txt', 'a')
    clean_rfid = ''
    for i in new_card.strip():
        if ord(i) > 47:
            clean_rfid += str(i)
    print clean_rfid
    file.write('newcard %s' %clean_rfid)
    file.write('\n')
    return 'Card added'







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
