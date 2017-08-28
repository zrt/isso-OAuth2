from flask import Flask,request,redirect
import config,json,requests
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
	r = requests.post('https://github.com/login/oauth/access_token',
		data={'client_id':config.client_id,
		'client_secret':config.client_secret,
		'code':code,
		'state':state},
		headers={'Accept':'application/json'})
	r = r.json()
	if 'access_token' not in r:
		return '[!] OAuth failed. code:5'
	token = r['access_token']
	r = requests.get('https://api.github.com/user',auth=('token',token))
	# print(r.json())
	r = r.json()

	try:
		content['email'] = r['email']
		content['website'] = r['avatar_url'] or 'http://www.gravatar.com/avatar/'+r['gravatar_id']
		content['website'] += ' '+r['html_url']
		content['author'] = r['name']
	except Exception as e:
		return '[!] OAuth data error. code:6'
	r['access_token'] = token

	# save content and r
	print(r)
	print(content)
	try:
		print(send_comment(content['uri'],content))
	except Exception as e:
		return '[!] OAuth link error. code:7'

	return '<html><head><meta charset="utf-8" /><title>Success!</title></head><body>Success.评论提交成功，正在等待审核，通过后会显示在评论区，5秒后此页面自动关闭。<script>setTimeout(function() {window.close()}, 5000);</script></body></html>'


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=28528)
