import flask
from flask import request, jsonify, url_for
import json
import requests
import urllib.parse
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import copy
from datetime import datetime

#from flask_jsonpify import jsonpify



import sys
import base64
from hashlib import md5
from Crypto import Random
from Crypto.Cipher import AES
from aes256 import aes256
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from flask import Response
import json
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


from Target import Target
from Targetvalue import Targetvalue
from levelapi import levelapi
from BudgetAllocation import BudgetAllocation
# from InsertRecSys import InsertRecSys



import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = flask.Flask(__name__)
app.debug = True


sentry_sdk.init(
    dsn="https://d4f55392a9aa4f78a816e498c88fb5c3@sentry.io/1873356",
    integrations=[FlaskIntegration()]
)





class PrefixMiddleware(object):
#class for URL sorting
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        #in this line I'm doing a replace of the word flaskredirect which is my app name in IIS to ensure proper URL redirect
        if environ['PATH_INFO'].lower().replace('/flaskredirect','').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/flaskredirect','')[len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/foo')



	
	
	
	
	
	
	
@app.route('/allocation')
def allocation():
    month = request.args['month']
    year = request.args['year']
    band = request.args['band']
    amount = request.args['amount']
    l0amount = request.args['l0amount']
    levels = request.args['levels']
    cityid = request.args['cityid']
    warehouseid = request.args['warehouseid']
    
    
    l0amount = int (l0amount)
    band = int (band)
    amount = int (amount)
    level = int (levels)
    warehouseid = int(warehouseid)
    cityid = int(cityid)
        


    jso=BudgetAllocation().allocate(month,year ,band,amount,l0amount,levels,cityid,warehouseid)
    #JSONP_data = jsonpify(jso)
    return jso

 
	
	
	
@app.route('/target/percent')
def target():
    
    percentage = request.args['percentage']
    levels = request.args['levels']
    ulimit = request.args['ulimit']
    llimit = request.args['llimit']
    #band = request.args['band']

    
    jso=Target().ret(percentage,levels,ulimit,llimit)
    #JSONP_data = jsonpify(jso)
    return jsonify(jso)
    
@app.route('/target/value')
def targetvalue():
    
    value = request.args['value']
    levels = request.args['levels']
    ulimit = request.args['ulimit']
    llimit = request.args['llimit']
    #band = request.args['band']

    jso=Targetvalue().ret(value,levels,ulimit,llimit)
    #JSONP_data = jsonpify(jso)
    return jsonify(jso)
	


@app.route('/levelling')
def levelling():
    
    month = request.args['month']
    year = request.args['year']
    level = request.args['level']
    
    jso=levelapi().api(month,year,level)
    return jsonify(jso)
	
    
    


if __name__ == '__main__':
    app.run()
