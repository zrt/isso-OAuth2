from flask import Flask,request,redirect
import config,json
from urllib.parse import quote_plus
from app import sign,send_comment
app = Flask('callback')

app.debug = False

# @app.route('/')
# def index():
# 	return 'cmt!'

@app.route('/',methods=['GET'])
def callback():
	# print(request.args)
	arg = dict(request.args)
	if 'state' not in arg:
		return '[!] OAuth failed. code:0'
	if 'content' not in arg:
		return '[!] OAuth failed. code:1'
	if 'code' not in arg:
		return '[!] OAuth failed. code:3'

	content = arg['content']
	if len(content) == 1:
		content = content[0]
	state = arg['state']
	if len(state) == 1:
		state = state[0]
	if state != sign(content):
		return '[!] OAuth failed. code:4'
	content = json.loads(content)
	code = arg['code']
	if len(code) == 1:
		code = code[0]
	r = request.post('https://github.com/login/oauth/access_token',
		data={'client_id':config.client_id,
		'client_secret':config.client_secret,
		'code':code},
		headers={'Accept':'application/json'})
	r = r.json()
	if 'access_token' not in r:
		return '[!] OAuth failed. code:5'
	token = r['access_token']
	r = request.get('https://api.github.com/user',auth=('token',token))
	print(r.json())
	return 'ok'


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=28528)
