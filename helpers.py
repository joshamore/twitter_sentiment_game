from twython import Twython
from twython import TwythonStreamer
from textblob import TextBlob
import datetime

# Don't push with keys!
consumer_key = 'and'
consumer_secret = 'and'
access_token = 'and'
access_secret = 'and'

# Stores stream tweet data 
streamTweet = []

# Setting up streamer
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        # Storing tweet if has a display picture and at least 100 tweets
        if data['user']['default_profile_image'] == False and data['user']["statuses_count"] > 100:
            streamTweet.append(data)
            self.disconnect()
            
    def on_error(self, status_code, data):
        # Prints status code and stops trying to get data on error
        print(status_code)
        self.disconnect()

# Will get a random Twitter user's details from the stream of most recent tweets
def getRandUser():
    # Resets streamTweet to ensure a new Twitter user is returned
    global streamTweet
    streamTweet = []
    
    # Setting auth
    stream = MyStreamer(consumer_key, consumer_secret, access_token, access_secret)
    
    # Filters tweets using negative words to give more balanced results (too postive with neutral language)
    stream.statuses.filter(track=['evil', 'hate', 'kill', 'justice'])
      
    # Storing user details
    userData = {
        'username': streamTweet[0]['user']['screen_name'],
        'bio': streamTweet[0]['user']['description'],
        'picture': streamTweet[0]['user']['profile_image_url']
    }
    
    # Returning user details
    return userData

# Pulling in tweets for given user
def pullTweets(user):
    # Setting auth
    twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)
    
    tweets = []
    
    # Pulling in user's most recent 50 tweets
    user_timeline = twitter.get_user_timeline(user_id=streamTweet[0]['user']['id'], count=50)
    for tweet in user_timeline:
        tweets.append(tweet['text'])
        
    return tweets

# Returns polarity analysis of passed tweets
def polarityAnalysis(tweets):
    polarity = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    
    # Generating polarity totals
    for tweet in tweets:
        tweetBlob = TextBlob(tweet)
        
        if tweetBlob.sentiment.polarity == 0:
            polarity['neutral'] += 1
        elif tweetBlob.sentiment.polarity > 0:
            polarity['positive'] += 1
        else:
            polarity['negative'] += 1
            
    return polarity
      
# Returns the total polarity of a passed array of Tweet text strings
# Weighs Tweets as positive or negative (1 or -1)
def totalPolarity(tweets):
    total = 0
    
    # Checking the polarity of each tweet
    for tweet in tweets:
        tweetBlob = TextBlob(tweet)
        if tweetBlob.sentiment.polarity < 0:
            total -= 1
        elif tweetBlob.sentiment.polarity > 0:
            total += 1
        
    return total