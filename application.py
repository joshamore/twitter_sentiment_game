import os
import sys
from flask import Flask, session, render_template, request, jsonify, redirect, url_for, redirect
from helpers import *
import sqlite3 as lite
from passlib.apps import custom_app_context as pwd_context

# To build from command line first: export FLASK_APP=application.py
# Then: flask run
# Docs for hash function: https://passlib.readthedocs.io/en/1.6.5/new_app_quickstart.html

# Setting up Flask app
app = Flask(__name__)
# Secret key used for session cookie
app.secret_key = os.urandom(24)

# Home page
@app.route('/')
def index():
    if 'username' in session:
        twitterUser = getRandUser()
        session['twitterUser'] = twitterUser['username']
        return render_template('index.html', twitterUser=twitterUser)
    else:
        return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Storing username and password variables from POST request
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Error checking that a username and password were submitted
        if not username:
            return render_template('error.html', errorCode = 'Username cannot be blank')
        elif not password:
            return render_template('error.html', errorCode = 'Password cannot be blank')

        # Ensures con is null before trying to establish a connection
        con = None
        
        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()

            # Queries DB for username provided by user
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            userData = cur.fetchone()
            
            # If username not found in DB, returns an error to user.
            # Otherwise, user found and checks password against stored hash.
            if not userData:
                return render_template('error.html', errorCode = 'Username not registered')
            else:
                # If password provided matches hash, sets session with username
                # Otherwise, throws an error
                if pwd_context.verify(password, userData[2]):
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    return render_template('error.html', errorCode = 'Incorrect password')
            
        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])
        
            sys.exit(1)
            
        finally:
            if con:
                con.close()

    else:
        return render_template('login.html')

# Positive guess
@app.route('/positiveGuess')
def positiveGuess():
    # Pulling Tweets for twitter user
    tweets = pullTweets(session['twitterUser'])
    
    # Storing polarity of tweets
    polarity = totalPolarity(tweets)
    
    # Will store the data to be passed back to client 
    results = {}
    
    # Date/time of guess will be stored in DB
    dateTime = datetime.datetime.now()
    dateTime = dateTime.replace(microsecond=0)
    
    # Calculating correctness of user's guess, updating DB, and rendering results page.
    if polarity >= 0:
        results['guess'] = 'correct'
        
        con = None
        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()
            
            # Executeds SQL query and commits to DB
            cur.execute("INSERT INTO guesses (username, twitter_user, guess, result, date) VALUES (?, ?, ?, ?, ?)", (session['username'], session['twitterUser'], 'positive', 'True', dateTime))
            con.commit()
            
            # Returns render with results
            return render_template('results.html', results = results)
        
        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])
        
            sys.exit(1)

        finally:
            if con:
                # Closes connection
                con.close()
    else:
        results['guess'] = 'incorrect'
                
        con = None
        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()
            
            # Executeds SQL query and commits to DB
            cur.execute("INSERT INTO guesses(username, twitter_user, guess, result, date) VALUES(?, ?, ?, ?, ?)", (session['username'], session['twitterUser'], 'positive', 'False', dateTime))
            con.commit()
            
            # Returns render with results
            return render_template('results.html', results = results)
        
        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])
        
            sys.exit(1)

        finally:
            if con:
                # Closes connection
                con.close()
    
# Negative guess
@app.route('/negativeGuess')
def negativeGuess():
    print("todo")
    
    return render_template('results.html')

# Accepts a GET request containg the username of a Twitter user and the app user's guess of Twitter user's sentiment
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

            # Setting session to log user in
            session['username'] = username
            
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

# Logs user out of account and returns to index
@app.route('/logout')
def logout():
    # Deletes data from session
    session.pop('username', None)
    session.pop('twitterUser', None)
    
    # Returns user to index
    return redirect(url_for('index'))

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