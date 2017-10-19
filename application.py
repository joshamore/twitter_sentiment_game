from textblob import TextBlob
import os
from flask import Flask, session, render_template
from helpers import *

app = Flask(__name__)

# Home page
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

# Register account page
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    #!! TODO !!
    # Move this functionality into helpers.py
    guessTweetData = pullTweets()
    
    # Checking the polarity of each tweet
    polarityCombo = 0
    for tweet in guessTweetData:
        tweetBlob = TextBlob(tweet)
        polarityCombo += tweetBlob.sentiment.polarity
        
    # TESTING
    print(guessTweetData[0])
    print(polarityCombo)
