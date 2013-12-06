#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# リストのTLを擬似ストリーミングで読み上げさせる
# 
# Author:   haya14busa
# URL:      http://haya14busa.com
# Require:  SayKotoeri, Saykana or SayKotoeri2
# License:  MIT License
# OS:       for Mac Only

import tweepy
from datetime import timedelta
import time
from subprocess import call
import re

from romaji2kana import romaji2katakana
import secret

import sys, codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def get_oauth():
    CONSUMER_KEY=secret.CONSUMER_KEY
    CONSUMER_SECRET=secret.CONSUMER_SECRET
    ACCESS_TOKEN_KEY=secret.ACCESS_TOKEN_KEY
    ACCESS_TOKEN_SECRET=secret.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth

### Replace String to Read Aloud###
def str_replace(string):
    string = re.sub('&.+;', ' ', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'ユーアールエル', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)
    string = re.sub(';', ' ', string)
    string = re.sub('`', ' ', string)

    string = re.sub('RT', 'リツイート', string)
    string = re.sub('♡', 'ハァト', string)
    string = re.sub('\?', '？', string)
    string = re.sub('\(|\)', ' ', string)
    return string

def showTL(api, read_id):
    try:
        tl = api.list_timeline('haya14busa', getArgs(), count=10, since_id = read_id)
        tl.reverse()
        for status in tl:
            status.created_at += timedelta(hours=9) # add 9 hours for Japanese time
            print u'---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                    name    = status.author.name,
                    screen  = status.author.screen_name,
                    text    = status.text,
                    src     = status.source,
                    created = status.created_at)
            read_text = str_replace(status.text.encode('utf_8'))
            read_text = romaji2katakana(read_text)
            read_text = read_text.replace('\n','')

            cmd = '~/bin/talk.sh "{text}"'.format(text=read_text)
            try:
                call(cmd, shell=True)
            except:
                print "SayKotoeri Couldn't read aloud"

        else:
            global lastSinceId
            lastSinceId = tl[-1].id
            
    except Exception, e:
        time.sleep(10)
        pass

def getArgs():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return 'vimvimvim'

def main():
    auth = get_oauth()
    api = tweepy.API(auth_handler=auth)
    lastGetTime = time.time() - 8
    global lastSinceId
    lastSinceId = None
    while True:
        if time.time() > lastGetTime + 8:
            lastGetTime = time.time()
            showTL(api, lastSinceId)
        else:
            time.sleep(1)

 
if __name__ == "__main__":
    main()
