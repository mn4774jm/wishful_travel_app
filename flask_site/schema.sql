DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS cache;
DROP TABLE IF EXISTS bookmarks;


-- Sample page for setting up db with sqlite3.
-- TODO reformat tables if sqlite3 is used; else replace with models and decide how best to connect
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_name TEXT NOT NULL,
    city TEXT NOT NULL unique,
    data TEXT NOT NULL,
    entry_date TIMESTAMP NOT NULL

);

CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL unique,
    state TEXT NOT NULL,
    wiki_entry TEXT NOT NULL,
    restaurants TEXT NOT NULL,
    directions TEXT NOT NULL,
    date TIMESTAMP NOT NULL

)
