import os
from flask import Flask, session, render_template, request, jsonify
from helpers import *

app = Flask(__name__)

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Will eventually have an if/else block to check if user is logged in
    # Returns data for a random user if logged in and request is GET
    if request.method == 'GET':
        twitterUser = getRandUser()
        return render_template('index.html', twitterUser=twitterUser)

# TESTING
@app.route('/test')
def twitterData():
    # Stores GET request argument in variable
    user = request.args.get('username')
    
    tweets = pullTweets(user)
    polarity = totalPolarity(tweets)
    
    return jsonify(polarity)
    

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
