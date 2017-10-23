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


# MAIN ONLY BEING USED FOR TESTING
if __name__ == '__main__':
    tweets = pullTweets()
    print(tweets[0])
    polarity = totalPolarity(tweets[1])
    
    # TESTING
    print(tweets[1][0])
    print(polarity)
