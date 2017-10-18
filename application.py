from twython import Twython
from twython import TwythonStreamer
from textblob import TextBlob

# Don't push with keys!
consumer_key = 'and'
consumer_secret = 'and'
access_token = 'and'
access_secret = 'and'

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

# Stores stream tweet data (including user)
streamTweet = []

# Setting up streamer
# Docs: http://twython.readthedocs.io/en/latest/usage/streaming_api.html?highlight=track#filtering-public-statuses
class MyStreamer(TwythonStreamer):
    
    def on_success(self, data):
        # Storing tweet if has a display picture and at least 100 tweets
        if data['user']['default_profile_image'] == False and data['user']["statuses_count"] > 100:
            streamTweet.append(data)
            self.disconnect()
    def on_error(self, status_code, data):
        print(status_code)
    
        # Stops trying to get data on error
        self.disconnect()

if __name__ == '__main__':
    # Setting stream auth
    stream = MyStreamer(consumer_key, consumer_secret, access_token, access_secret)
    
    # TEST FILTER
    stream.statuses.filter(track=['the', 'of', 'to', 'and', 'in', 'you', 'that', 'it', 'is', 'for'])
    
    #Storing tweets text
    guessTweetData = []
    
    # Pulling in user tweets
    user_timeline = twitter.get_user_timeline(user_id=streamTweet[0]['user']['id'], count=50)
    for tweet in user_timeline:
        guessTweetData.append(tweet['text'])
        
    # Checking the polarity of each tweet
    polarityCombo = 0
    for tweet in guessTweetData:
        tweetBlob = TextBlob(tweet)
        polarityCombo += tweetBlob.sentiment.polarity
        
    # TESTING
    print(guessTweetData[0])
    print(polarityCombo)