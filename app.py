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
    baseurl = "https://api.coinmarketcap.com/v1/ticker/"
 
    
    
    
    resultall = urllib.request.urlopen(baseurl).read()
    
    data = json.loads(resultall)
    
    
    res = makeWebhookResult(data, req)
    return res


    


def makeWebhookResult(data, req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    currency = parameters.get("currency")
    
    if currency == "Bitcoin":
        data1=data[0]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Ethereum"
        data1=data[1]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Dash"
        data1=data[2]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Monero"
        data1=data[3]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Litecoin"
        data1=data[5]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Ripple"
        data1=data[4]
        name=data1.get('name')
        price=data1.get('price_usd')
    if currency == "Zcash"
        data1=data[11]
        name=data1.get('name')
        price=data1.get('price_usd')
        

   # astronomy=weather.get('astronomy')

    




   #  print(json.dumps(item, indent=4))

    speech = "Currently "+ name +" is at " +price + " Dollars"

    
   

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {
            "google": {
                "expect_user_response": "false",
                 }
            }

          }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
