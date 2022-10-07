# twitter_sentiment_game
This is my final project submission for <a href="https://www.edx.org/course/introduction-computer-science-harvardx-cs50x">CS50x</a> (Harvard/edx).

## The project
A game that requires you to guess the Tweet sentiment of a random Twitter user based their username, display picture, and bio.

**<a href="https://twittersentimentgame.joshamore.com/" target="_blank">Play here</a>.**

## This Repo
This is the production version of the project. The development branch is <a href="https://github.com/joshamore/twitter_sentiment_game/tree/master">here</a>. The main difference is the use of SQLite3 in development and PostgreSQL in production.

## Languages, Libraries, and Tools
**Backend**
* <a href="https://www.python.org/download/releases/3.0/">Python 3.x</a> - Backend language.
* <a href="http://flask.pocoo.org/">Flask</a> - Backend microframework.
* <a href="https://www.postgresql.org/">PostgreSQL</a> - Database used for the deployed app.
    * <a href="https://www.sqlite.org/">SQLite</a> - Database used for development (easier to make quick changes and setup).
* <a href="https://twython.readthedocs.io/en/latest/">Twython</a> - Python API wrapper.
* <a href="https://textblob.readthedocs.io/en/dev/">TextBlob</a> - A library that helps with natural language processing (NLP). Used for sentiment analysis.
* <a href="https://passlib.readthedocs.io/en/stable/">Passlib</a> - Assisted with password hashing.

**Frontend**
* <a href="https://jquery.com/">jQuery</a> - JavaScript helper library.
* <a href="https://getbootstrap.com/">Bootstrap</a> - CSS framework.

**General**
* <a href="https://www.heroku.com/">Heroku</a> - Cloud app hosting - moved to self hosting due to nuked free-tier.
