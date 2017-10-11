from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = 'cfgvhb'
consumer_secret = 'cbv '
access_token = 'cvbn'
access_token_secret = 'cvbn'

# Stores tweets
tweets = []

#This is a basic listener that stores tweet in list until 10 are present
class StdOutListener(StreamListener):

    def on_data(self, data):
        if len(tweets) < 10:
            tweets.append(data)
            return True
        else:
            return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listen = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listen)

    # Stream filter for all lowercase roman alphabet letters
    stream.filter(track=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])

    # TESTING
    print(len(tweets))
    print(tweets[0])