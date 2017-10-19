from textblob import TextBlob
from Flask import Flask
from helpers import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world'


if __name__ == '__main__':
    guessTweetData = pullTweets()
    
    # Checking the polarity of each tweet
    polarityCombo = 0
    for tweet in guessTweetData:
        tweetBlob = TextBlob(tweet)
        polarityCombo += tweetBlob.sentiment.polarity
        
    # TESTING
    print(guessTweetData[0])
    print(polarityCombo)