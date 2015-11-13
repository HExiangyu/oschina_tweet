#!/usr/local/bin/python
#  coding: utf-8
import sys
import ConfigParser
import json
import urllib
import urllib2
import time

__author__ = 'hxy'

reload(sys)
sys.setdefaultencoding( "utf-8" )

second_time = 60*60*8
login_api = 'http://www.oschina.net/action/user/hash_login'
tweet_api = 'http://www.oschina.net/action/tweet/pub'
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56"


def init():
    global user
    global email
    global pwd
    global user_code
    conf = ConfigParser.ConfigParser()
    conf.read("init.conf")
    user = conf.get("init", "user")
    email = conf.get("init", "email")
    pwd = conf.get("init", "pwd")
    user_code = conf.get("init", "user_code")
    print 'init success \n'


def login():
    global my_cookie
    values = {'email': email, 'pwd': pwd}
    values = urllib.urlencode(values)
    request = urllib2.Request(login_api, values)
    request.add_header("User-Agent", user_agent)
    response = urllib2.urlopen(request)
    my_cookie = response.headers["Set-cookie"]
    print 'login success \n'


def tweet( msg ):
    values = {'user': user, 'user_code': user_code, 'msg': msg}
    values = urllib.urlencode(values)
    request = urllib2.Request(tweet_api, values)
    request.add_header("User-Agent", user_agent)
    request.add_unredirected_header('Cookie', my_cookie)
    response = urllib2.urlopen(request)
    print response.read()
    print "tweet post success \n"

def api():
    api_key = "4c2667a1772b14c6a222cb351985a5c5"
    uri_api = "http://www.tuling123.com/openapi/api?key=" + api_key + "&info=讲个笑话"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56"
    request = urllib2.Request(uri_api)
    request.add_header("User-Agent", user_agent)
    response = urllib2.urlopen(request)
    obj = response.read()
    encode_json = json.loads(obj)
    code = encode_json.get('code')
    if code == 100000:
        text = encode_json.get('text')
        print text
    else:
        text = 'oh,my god, the api fail'
    return text

def main():
    print 'start: \n'
    msg = api()
    msg = msg.replace("<br>", " ")
    msg = msg[0:158]
    init()
    login()
    tweet(msg)
    print 'run success \n'

def task( second ):
    while True:
        main()
        time.sleep(second)

task(second_time)





