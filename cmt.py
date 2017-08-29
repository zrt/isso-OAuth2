#! python3
# -*- coding: utf-8 -*- 
from flask import Flask,request,redirect
import config,json
from urllib.parse import quote_plus
from app import sign
app = Flask('cmt')

app.debug = False

# @app.route('/')
# def index():
# 	return 'cmt!'

@app.route('/new',methods=['GET'])
def new():
	# print(request.json)
	uri = request.args.get('uri')
	#r = request.json
	# print(request.args.get('data'))
	r = json.loads(request.args.get('data'))
	r['uri']=uri
	content = json.dumps(r)
	url = 'https://github.com/login/oauth/authorize?client_id='+config.client_id
	url += '&redirect_uri=' +quote_plus(config.redirect_uri + '?content=' + quote_plus(content))
	url += '&scope='+'user:email'
	url += '&state=' + sign(content) 
	return redirect(url)


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=28527)
