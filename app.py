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
    baseurl = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=41c9cef29f974bd48c2192134173101&format=json&q="
 
    
    query = getCoor(req)
    surl = baseurl + query
    result = urllib.request.urlopen(surl).read()

    data = json.loads(result)

    res = makeWebhookResult(data)
    return res


#def makeYqlQuery(req):
  #  result = req.get('result')
    
 #   if result is None:
 ##       return{}
   
   # city = parameters.get('geo-city')
  #  beach = parameters.get('beach')
#    coord = getCoor(req)
   
   # if beach == "north shore":
   #     coor = "20.934431,-156.355957&tp=24"
   # if beach == "south shore":
   #     coor ="20.626836,-156.443873&tp=24"
   # if beach == "west shore":
   #     coor ="20.864596,-156.673628&tp=24"
   # if beach == "east shore":
   #     coor = "20.759070,-155.985446&tp=24"

 #   return coord
    
#    if city is None:
#        return None

#    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def getCoor(data):
    
    result = data.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    beach = parameters.get("beach")
    
    if beach == "north shore":
        coor = "20.934431,-156.355957&tp=24"
        return coor
    if beach == "south shore":
        coor ="20.626836,-156.443873&tp=24"
        return coor
    if beach == "west shore":
        coor ="20.864596,-156.673628&tp=24"
        return coor
    if beach == "east shore":
        coor = "20.759070,-155.985446&tp=24"
        return coor

       
    citybaseurl="http://maps.googleapis.com/maps/api/geocode/json?address="
    queryurl=citybaseurl + city
    query = urllib.request.urlopen(queryurl).read()
    info = json.loads(query)
    results=info.get('results')
    zero=results[0]
#    city1=zero.get("address_components")
#    zero2=city1[0]
    
  #  if zero2.get('long_name')=='Honolulu'
 #       return "20.934431,-156.355957&tp=24"
    
    geometry=zero.get('geometry')
    location=geometry.get('location')
      #  lat=location.get('lat')
       # longi=location.get('lng')
        
    coor= location.get('lat') + location.get('lng')+ "&tp=24"
    
    return coor


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

    speech = "Currently it is " + hourly1.get('swellHeight_ft') + " feet"

    
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
