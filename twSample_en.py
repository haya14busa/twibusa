# -*- coding: utf-8 -*-
# http://newbienewbie.wordpress.com/2011/04/16/twitterのstreaming-apiを試してみる/
 
import sys
import tweepy
import re
import secret

import sys, codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
 
Q = sys.argv[1:]
 
def get_oauth():
    CONSUMER_KEY=secret.CONSUMER_KEY
    CONSUMER_SECRET=secret.CONSUMER_SECRET
    ACCESS_TOKEN_KEY=secret.ACCESS_TOKEN_KEY
    ACCESS_TOKEN_SECRET=secret.ACCESS_TOKEN_SECRET
     
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth

class CustomStreamListener(tweepy.StreamListener):
     
    def on_status(self, status):
         
        try:
            # 漢字、ひらがな、カタカナが一文字でもあれば簡易的に日本語のTLとする
            if(re.match(u'[一-龠]+|[ぁ-ん]+|[ァ-ヴー]+', status.text.encode('utf_8'))):
                pass
            else:
                 
                print "%s\t%s\t%s\t%s" % (status.text.encode('utf-8'),
                                          status.author.screen_name.encode('utf-8'),
                                          status.created_at,
                                          status.source.encode('utf-8'),)
                f = open('twitter_en.txt', 'a')
                str = status.text.encode('utf-8') + '\n'
                f.write(str)
                f.close()
                 
        except Exception, e:
            print >> sys.stderr, 'Encounted Exception:', e
            pass
         
    def on_error(self, status_code):
         
        print >> sys.stderr, 'Encounted Exception with status code:', status_code
        return True
     
    def on_timeout(self):
         
        print >> sys.stderr, 'Timeout...'
        return True
 


# streaming_api = tweepy.Stream('ユーザ名', 'パスワード', CustomStreamListener(), timeout=None)
 
# print >> sys.stderr, 'Filtering the public timeline for "%s"' % (''.join(sys.argv[1:]),)
 
#Public TLからワードを指定して取り出す場合、引数にワードを指定し、この関数を利用する
#streaming_api.filter(follow=None, track=Q)
 
#何も指定せず、ただPublic TLのみを取り出す場合は、この関数を利用する
# streaming_api.sample()
  
def main():
    auth = get_oauth()
    stream = tweepy.Stream(auth, CustomStreamListener())
    stream.timeout = None
    if len(Q) == 0:
        stream.sample()
    else:
        stream.filter(follow=None, track=Q)
 
if __name__ == "__main__":
    main()
