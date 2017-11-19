# twitter_sentiment_game
This is my final project submission for <a href="https://www.edx.org/course/introduction-computer-science-harvardx-cs50x">CS50x</a> (Harvard/edx).

## The project
A game that requires you to guess the Tweet sentiment of a random Twitter user based their username, display picture, and bio.

**<a href="https://goo.gl/UX8Lp2">Play here</a>.**

## This Repo
This is the development version of the project. The production branch is <a href="https://github.com/joshamore/twitter_sentiment_game/tree/heroku_deployed">here</a>. The main difference is the use of SQLite3 in development and PostgreSQL in production.

## Languages, Libraries, and Tools
**Backend**
* Python/Flask - Main backend language and framework.
* PostgreSQL - Database used for the deployed app.
    * SQLite - Database used for development (easier to make quick changes and setup).
* Twython - Python API wrapper.
* TextBlob - A library that helps with natural language processing (NLP). Used for sentiment analysis.
* Passlib - Assisted with password hashing.

**Frontend**
* jQuery - JavaScript helper library.
* Bootstrap - CSS framework.

**General**
* Heroku - Cloud app hosting.