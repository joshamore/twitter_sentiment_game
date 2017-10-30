import os
from flask import Flask, session, render_template, request, jsonify
from helpers import *

app = Flask(__name__)

# DB TESTING START
    #TODO
# DB TESTING END 
    
# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Will eventually have an if/else block to check if user is logged in
    # Returns data for a random user if logged in and request is GET
    if request.method == 'GET':
        twitterUser = getRandUser()
        return render_template('index.html', twitterUser=twitterUser)

# Accepts a GET request containg the username of a Twitter user and the app user's guess of Twitter user's
# Sentiment
@app.route('/twitterdata')
def twitterData():
    # Stores GET request arguments in variables
    user = request.args.get('username')
    guess = request.args.get('guess')
    
    tweets = pullTweets(user)
    polarity = totalPolarity(tweets)
    
    results = {
        'polarity': polarity,
        'results': guess
    }
        
    return jsonify(results)
    
# Returns a page displaying the results of a user's guess
# TODO: Need to link up with JS.
@app.route('/results')
def results():
    return render_template('results.html')
    
# Register account page
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# MAIN ONLY BEING USED FOR TESTING
if __name__ == '__main__':
    user = getRandUser()
    tweets = pullTweets(user['username'])
    polarity = totalPolarity(tweets)
    
    # TESTING
    print(user)
    print(tweets[0])
    print(polarity)
