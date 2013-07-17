#!/usr/bin/python
# -*- coding:utf-8 -*-

import tweepy
import secret

CONSUMER_KEY=secret.CONSUMER_KEY
CONSUMER_SECRET=secret.CONSUMER_SECRET
ACCESS_TOKEN_KEY=secret.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET=secret.ACCESS_TOKEN_SECRET
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth_handler=auth)
