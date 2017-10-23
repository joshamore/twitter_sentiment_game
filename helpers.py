from twython import Twython
from twython import TwythonStreamer
from textblob import TextBlob

# Don't push with keys!
consumer_key = 'and'
consumer_secret = 'and'
access_token = 'and'
access_secret = 'and'

# Stores stream tweet data (including user)
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

# Will pull in 50 most recent tweets from a random user
def pullTweets():
    # Setting auths
    twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)
    stream = MyStreamer(consumer_key, consumer_secret, access_token, access_secret)
    
    # Filters tweets checking for 10 most common english words
    stream.statuses.filter(track=['the', 'of', 'to', 'and', 'in', 'you', 'that', 'it', 'is', 'for'])
    
    guessTweetData = []
    returnData = []
    
    # Pulling in user tweets
    user_timeline = twitter.get_user_timeline(user_id=streamTweet[0]['user']['id'], count=50)
    for tweet in user_timeline:
        guessTweetData.append(tweet['text'])
        
    # Storing user details
    userData = {
        'username': streamTweet[0]['user']['screen_name'],
        'bio': streamTweet[0]['user']['description'],
        'picture': streamTweet[0]['user']['profile_image_url']
    }
    
    # Storing user data and tweet data in a list to be returned
    returnData.append(userData)
    returnData.append(guessTweetData)
    
    # Returning text of past 50 tweets in a list
    return returnData

# Returns the total polarity of a passed array of tweet text strings
def totalPolarity(tweets):
    total = 0
    
    # Checking the polarity of each tweet
    for tweet in tweets:
        tweetBlob = TextBlob(tweet)
        total += tweetBlob.sentiment.polarity
        
    return total
