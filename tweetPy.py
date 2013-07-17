#!/usr/bin/python
# -*- coding:utf-8 -*-

import tweepy
import sys, codecs
import secret

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



def main():
    auth = get_oauth()
    api = tweepy.API(auth_handler=auth)

    tweet = ""
    if len(sys.argv) < 2:
        tweet = raw_input("Tweet:")
    else:
        for i in range(len(sys.argv)):
            if i == 0:
                continue
            tweet = tweet + " " + sys.argv[i] 

    api.update_status(tweet)
 
if __name__ == "__main__":
    main()
