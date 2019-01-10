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
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    currency = parameters.get("currency")
    
    
    
    baseurl = "https://api.coinmarketcap.com/v1/ticker/"
    surl = baseurl + currency
    
    
    
    resultall = urllib.request.urlopen(surl).read()
    
    data = json.loads(resultall)
    
    
    res = makeWebhookResult(data)
    return res



def makeWebhookResult(data):
    

    data1=data[0]
    name=data1.get('name')
    price=data1.get('price_usd')   

   # astronomy=weather.get('astronomy')

    




   #  print(json.dumps(item, indent=4))

    speech = "Currently "+ name +" is at " +price + " US Dollars"

    
    sessionId = req.get("sessionId")
    contexts = req.get("contexts")
    contextName = contexts.get("name")
    print("Response:")
    print(speech)
    
    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
               {
                 "text": [
                   speech
                  ],
               }
                  ],
        "payload": {
            "google": {
                "expect_user_response": "false",
                
                
                
             
                 }
            "outputContexts": [
                {
                    "name": "projects/testsatoshi-64f93/agent/sessions/" + sessionId + "/contexts/" + contextName,
                    "lifespanCount": 5,
                     
                }
            }

          }
        
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
