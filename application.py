import os
import sys
from flask import Flask, session, render_template, request, jsonify
from helpers import *
import sqlite3 as lite
from passlib.apps import custom_app_context as pwd_context

# To build from command line first: export FLASK_APP=application.py
# Then: flask run
# Docs for hash function: https://passlib.readthedocs.io/en/1.6.5/new_app_quickstart.html

app = Flask(__name__)

# DB TESTING START -- REMOVE AFTER COMPLETING REGISTER FUNCTION
con = None

try:
    con = lite.connect('twittergame.db')

    cur = con.cursor()
    cur.execute('SELECT "username" FROM users WHERE id=1')
    #cur.execute("INSERT INTO users(username, hash) VALUES('ssadasi', 'assaaasasfsas')")
    #con.commit()

    data = cur.fetchone()
    print(data[0])

except lite.Error as e:
    print('Error: {}'.format(e.args[0]))
    sys.exit(1)

finally:
    if con:
        con.close()
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
    # POST method means user has submitted a form (creating an account).
    # GET returns a render of the page.
    if request.method == 'POST':
        # Stores form data received from POST request
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Error checking that a username and password were submitted
        if not username:
            return render_template('error.html', errorCode = 'Username cannot be blank')
        elif not password:
            return render_template('error.html', errorCode = 'Password cannot be blank')
        
        # TODO: Check that username doesn't already exist (throw error if so)
        # TODO: If user is unique, hash password and store in users table. Then return to index logged in to new account.
        # TODO: Will need to setup session before user can login.
        
        return render_template('register.html')
    else:
        return render_template('register.html')


# MAIN ONLY BEING USED FOR TESTING
if __name__ == '__main__':
    user = getRandUser()
    tweets = pullTweets(user['username'])
    polarity = totalPolarity(tweets)
    
    # Password testing
    dank = input("Yes? ")
    
    hasha = pwd_context.encrypt(dank)
    
    print("Hashed:" + hasha)
    
    verify = pwd_context.verify(dank, hasha)
    
    print(verify)