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
    # Generates a random Twitter user (name, picture, and bio) if session active
    if 'username' in session:
        twitterUser = getRandUser()
        session['twitterUser'] = twitterUser['username']
        
        return render_template('index.html', twitterUser=twitterUser)
    # If no active session sends to login
    else:
        return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirects user to main game screen if session active
    if 'username' in session:
        return redirect(url_for('index'))
    # Attempts to login user if session inactive
    else:
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
@app.route('/positiveguess')
def positiveGuess():
    # Processes positive guess if session active
    if 'username' in session:
        # Pulling Tweets for Twitter user
        tweets = pullTweets(session['twitterUser'])

        # Storing polarity of Tweets
        polarity = totalPolarity(tweets)
        
        # Stores data to be passed back to client 
        results = {}

        results['guess'] = 'Positive'

        # Date/time of guess will be stored in DB
        dateTime = datetime.datetime.now()
        dateTime = dateTime.replace(microsecond=0)

        # Calculating correctness of user's guess, updating DB, and rendering results page.
        if polarity >= 0:
            results['answer'] = 'Correct'

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
            results['answer'] = 'Incorrect'

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
    # Sends user to login if no session set
    else:
        return redirect(url_for('login'))
    
# Negative guess
@app.route('/negativeguess')
def negativeGuess():
    # Processes negative guess if session active
    if 'username' in session:
        # Pulling Tweets for Twitter user
        tweets = pullTweets(session['twitterUser'])

        # Storing polarity of Tweets
        polarity = totalPolarity(tweets)

        # Will store the data to be passed back to client 
        results = {}

        results['guess'] = 'Negative'

        # Date/time of guess will be stored in DB
        dateTime = datetime.datetime.now()
        dateTime = dateTime.replace(microsecond=0)

        # Calculating correctness of user's guess, updating DB, and rendering results page.
        if polarity >= 0:
            results['answer'] = 'Incorrect'

            con = None
            try:
                # Establishes connection to DB
                con = lite.connect('twittergame.db')
                # Sets cursor for connected DB
                cur = con.cursor()

                # Executeds SQL query and commits to DB
                cur.execute("INSERT INTO guesses (username, twitter_user, guess, result, date) VALUES (?, ?, ?, ?, ?)", (session['username'], session['twitterUser'], 'negative', 'False', dateTime))
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
            results['answer'] = 'Correct'

            con = None
            try:
                # Establishes connection to DB
                con = lite.connect('twittergame.db')
                # Sets cursor for connected DB
                cur = con.cursor()

                # Executeds SQL query and commits to DB
                cur.execute("INSERT INTO guesses(username, twitter_user, guess, result, date) VALUES(?, ?, ?, ?, ?)", (session['username'], session['twitterUser'], 'negative', 'True', dateTime))
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
    # Sends user to login if no session set
    else:
        return redirect(url_for('login'))
    
# Accepts a GET request containg the username of a Twitter user and the app user's guess of Twitter user's sentiment
@app.route('/twitterdata')
def twitterData():
    # Confirms active session
    if 'username' in session:
        tweets = pullTweets(session['twitterUser'])
        polarity = polarityAnalysis(tweets)

        return jsonify(polarity)
    # Sends user to login if no active session
    else:
        return redirect(url_for('index'))
    
# Register account page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Returns user to main game screen if session active
    if 'username' in session:
        return redirect(url_for('index'))
    # Attempts to create a new account if no active session
    else:
        # POST method means user has submitted a form (creating an account)
        # GET returns a render of the page
        if request.method == 'POST':
            # Stores form data received from POST request
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

                # Executeds SQL query (storing username and password has)
                cur.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (username, pwd_context.encrypt(password)))
                
                # Commits changes to DB
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
        else:
            return render_template('register.html')

# Displays user's past guess history
@app.route('/history')
def history():
    # Allows user to access history if session active
    if 'username' in session:
        # Ensures con is null before trying to establish a connection
        con = None

        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()

            # Queries DB for guess entries for user and stores all in userHistory
            cur.execute("SELECT * FROM guesses WHERE username = ?", (session['username'],))
            userHistory = cur.fetchall()

            # Renders page and passes template guesses in a list
            return render_template('history.html', history = userHistory)

        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])

            sys.exit(1)

        finally:
            if con:
                con.close()
    # Sends user to login if no session active
    else:
        return redirect(url_for('index'))

# Returns history guess data
@app.route('/historyguessdata')
def historyGuessData():
    # Ensures session active
    if 'username' in session:
        # Ensures con is null before trying to establish a connection
        con = None

        try:
            # Establishes connection to DB
            con = lite.connect('twittergame.db')
            # Sets cursor for connected DB
            cur = con.cursor()

            # Queries DB for user's guess entries and stores userHistory (as a list of tuples)
            cur.execute("SELECT result FROM guesses WHERE username = ?", (session['username'],))
            userHistory = cur.fetchall()

        except lite.Error as e:
            # Prints error on server side and renders error code for user
            print('Error: {}'.format(e.args[0]))
            return render_template('error.html', errorCode = e.args[0])

            sys.exit(1)

        finally:
            if con:
                con.close()
    
        # Data will be returned in a list of two elements, with the first element being correct guesses and
        # the second being incorrect guesses
        returnData = [0, 0]

        # Updates returnData based on guess data for each stores DB tuple
        for item in userHistory:
            if item[0] == 'True':
                returnData[0] += 1
            else:
                returnData[1] += 1

        # Returns list as JSON to client
        return jsonify(returnData)
    # Sends user to login if no session active
    else:
        return redirect(url_for('index'))

# Logs user out of account and returns to index
@app.route('/logout')
def logout():
    # Drops session if a session is active
    if 'username' in session:
        # Deletes data from session
        session.pop('username', None)
        session.pop('twitterUser', None)

        # Returns user to login
        return redirect(url_for('login'))
    # Redirects user to login if no active session
    else:
        return redirect(url_for('login'))

# Error handling for 404 errors (page not found)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404