DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

DROP TABLE IF EXISTS guesses;
CREATE TABLE guesses (
    username TEXT NOT NULL,
    twitter_user TEXT NOT NULL,
    guess TEXT NOT NULL,
    result TEXT NOT NULL,
    date TEXT NOT NULL
);