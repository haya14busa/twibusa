#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Timelineをストリーミングで読み上げさせる
# 
# Author:   haya14busa
# URL:      http://haya14busa.com
# require:  SayKotoeri, Saykana or SayKotoeri2
# OS:       for Mac Only
# Link:     [twitterをターミナル上で楽しむ(python)](http://www.nari64.com/?p=200)
 
import tweepy
from tweepy import  Stream, TweepError
import logging
import urllib
from datetime import timedelta
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

def str_replace(string):
    string = re.sub('&.+;', ' ', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'ユーアールエル', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)

    string = re.sub('RT', 'リツイート', string)
    string = re.sub('♡', 'ハァト', string)
    string = re.sub('\?', '？', string)
    string = re.sub('\(|\)', ' ', string)
    return string

class CustomStreamListener(tweepy.StreamListener):
 
    def on_status(self, status):
 
        try:
            status.created_at += timedelta(hours=9) # add 9 hours for Japanese time
            print u'---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                    name = status.author.name,
                    screen = status.author.screen_name,
                    text = status.text,
                    src = status.source,
                    created = status.created_at)
            read_text = str_replace(status.text.encode('utf-8'))
            read_text = romaji2katakana(read_text)

            # cmd = 'SayKotoeri2 -p aq_rb2 -b 80 -s 120 "{text}" >/dev/null 2>&1'.format(text=read_text)
            cmd = 'SayKotoeri -s "-s 120" "{text}" >/dev/null 2>&1'.format(text=read_text)
            try:
                call(cmd, shell=True)
            except:
                print "SayKotoeri Couldn't read aloud"

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass
 
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream
 
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream
 
 
class UserStream(Stream):
  
    def user_stream(self, follow=None, track=None, async=False, locations=None):
        self.parameters = {"delimited": "length", }
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
 
        if self.running:
            raise TweepError('Stream object already connected!')
 
        self.scheme = "https"
        self.host = 'userstream.twitter.com'
        self.url = '/2/user.json'
 
        if follow:
           self.parameters['follow'] = ','.join(map(str, follow))
        if track:
            self.parameters['track'] = ','.join(map(str, track))
        if locations and len(locations) > 0:
            assert len(locations) % 4 == 0
            self.parameters['locations'] = ','.join(['%.2f' % l for l in locations])
 
        self.body = urllib.urlencode(self.parameters)
        logging.debug("[ User Stream URL ]: %s://%s%s" % (self.scheme, self.host, self.url))
        logging.debug("[ Request Body ] :" + self.body)
        self._start(async)
  
def main():
    auth = get_oauth()
    stream = UserStream(auth, CustomStreamListener())
    stream.timeout = None
    stream.user_stream()
 
if __name__ == "__main__":
    main()
