#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    baseurl = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=41c9cef29f974bd48c2192134173101&format=json&"
    #result= "data,: request"
    
    query = makeYqlQuery(req)
    surl = baseurl + urllib.parse.urlencode({'q': query})
    result = urllib.request.urlopen(surl).read()
    #result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    #data="hey"
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
      result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        beach = parameters.get("beach")
    if beach is "north shore":
        return "20.934431,-156.355957&tp=24"

    return "20.626836,-156.443873&tp=24"
    
#    if city is None:
#        return None

#    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    
    data1=data.get('data')
   # data2=data1.get('data')
    #request=data2.get('request')
    weather=data1.get('weather')
    zero=weather[0]
    hourly=zero.get('hourly')
    hourly1=hourly[0]
   # astronomy=weather.get('astronomy')




   #  print(json.dumps(item, indent=4))

    speech = "Whoa its " + hourly1.get('swellHeight_ft') + "feet"

    
   # speech = "Hello there" 
   

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
     #    "data": astronomy,
      #  "weather" weather
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
