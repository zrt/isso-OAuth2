#! python3

import requests
import json,config
from urllib.parse import quote_plus
import hashlib

def send_comment(uid,cmt):
    host = config.host_url
    cmt['secret'] = config.comment_secret
    r = requests.post(host+quote_plus(uid),json=cmt)
    print(r.text)

def sign(s):
    md5 = hashlib.md5((s+'|233|'+config.server_secret).encode('utf-8')).hexdigest()
    return md5

