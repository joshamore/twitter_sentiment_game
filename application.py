from twython import Twython
from twython import TwythonStreamer

# Don't push with keys!
consumer_key = 'sdasd'
consumer_secret = 'asdasd'
access_token = 'asdas'
access_secret = 'asdasd'


# Stores tweets
tweets = []

# Setting up streamer
# Docs: http://twython.readthedocs.io/en/latest/usage/streaming_api.html?highlight=track#filtering-public-statuses
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        # Storing tweet if less than 10, otherwise disconnecting
        if len(tweets) < 10:
            tweets.append(data)
        else:
            self.disconnect()

    def on_error(self, status_code, data):
        print status_code
        
        # Stops trying to get data on error
        self.disconnect()
        
if __name__ == '__main__':
    # Setting stream auth
    stream = MyStreamer(consumer_key, consumer_secret, access_token, access_secret)
    
    # Grabbing currnet tweets that contain a lowercase letter
    stream.statuses.filter(track='a')
    
    # TESTING
    print(tweets[0])
    print(tweets[0]['text'])
    print(len(tweets))