import os
import sys
from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from helpers import *
import sqlite3 as lite
from passlib.apps import custom_app_context as pwd_context

# To build from command line first: export FLASK_APP=application.py
# Then: flask run
# Docs for hash function: https://passlib.readthedocs.io/en/1.6.5/new_app_quickstart.html

app = Flask(__name__)
# Secret key used for session cookie
app.secret_key = os.urandom(24)

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            return "TODO"
        else:
            twitterUser = getRandUser()
            return render_template('index.html', twitterUser=twitterUser)
    else:
        redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "todo"
        #TODO: Setup login session
    else:
        return render_template('login.html')

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
        
        con = None
        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()
            
            # Executeds SQL query (storing username and password has). Must commit to push changes to DB
            cur.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (username, pwd_context.encrypt(password)))
            con.commit()

            # TODO: Need to create a new session for the user!!!!!
            
            # Redirects to index/home
            return redirect(url_for('index'))
        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])
        
            sys.exit(1)

        finally:
            if con:
                # Closes connection
                con.close()
                
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