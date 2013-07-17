#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy
import re
from subprocess import call
import secret
import sys
# import sys, codecs
# 
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)
 
 
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
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'URL', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)

    string = re.sub('RT', 'Retweet', string)
    return string

class CustomStreamListener(tweepy.StreamListener):
     
    def on_status(self, status):
         
        try:
            # 漢字、ひらがな、カタカナが一文字でもあれば簡易的に日本語のTLとする
            if(re.match(u'[一-龠]+|[ぁ-ん]+|[ァ-ヴー]+', status.text)):
                pass
            else:
                print '---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                        name = status.author.name,
                        screen = status.author.screen_name,
                        text = status.text,
                        src = status.source,
                        created = status.created_at)
                read_text = str_replace(status.text)
                call(['say "{text}"'.format(text=read_text.encode('utf-8'))], shell=True)
                 
        except Exception, e:
            # print >> sys.stderr, 'Encounted Exception:', e # maybe contains Japanese
            pass
         
    def on_error(self, status_code):
         
        print >> sys.stderr, 'Encounted Exception with status code:', status_code
        return True
     
    def on_timeout(self):
         
        print >> sys.stderr, 'Timeout...'
        return True
  
def main():
    auth = get_oauth()
    stream = tweepy.Stream(auth, CustomStreamListener())
    stream.timeout = None
    Q = sys.argv[1:]
    if len(Q) == 0:
        Q = raw_input('Search words: ')
        # stream.sample()
    stream.filter(follow=None, track=Q)
 
if __name__ == "__main__":
    main()
