import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import json
from tweepy.streaming import StreamListener

consumer_key = 'qseJxWFBApOx2mTuc35u8sC1z'
consumer_secret = '9oUubdXuVrrkr1p6ZDtVWmS8JtwJ9HiVdBxdsUHUbHESoN9qgY'
access_token = '565871988-P2iIVjaMDSYC81fWB0AyNeepZKHZhNqlcunXPejJ'
access_secret = '7kNrllifTi2lF7zG1Tx9M64O9MLgi0keC6mZQ8HllEwNh'

keyword="film"

try:
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
except:
    print("Error: Authentication Failed")

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('Datasets/'+keyword+'.json', 'a') as f:
                tweet = json.loads(data)
                if tweet["lang"] == "en":
                   #print(data)
                   f.write(data)
                else:
                   print("not english: "+tweet["text"])
            return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def stream_tweets(keyword):
    twitter_stream = Stream(auth, MyListener())
    keywords = [keyword, "#" + keyword.replace(' ', '_'), keyword.join(' '), keyword+' movie', "#" + keyword.replace(' ', '_')+'_'
                                                                                                                               'movie']
    twitter_stream.filter(track=keywords, async=True)

stream_tweets('the godfather')