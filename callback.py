from flask import Flask,request,redirect
import config,json
from urllib.parse import quote_plus
from app import sign
app = Flask('callback')

app.debug = False

# @app.route('/')
# def index():
# 	return 'cmt!'

@app.route('/',methods=['GET'])
def callback():
	print(request.args)
	return 'ok'


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=28528)
