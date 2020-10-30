
DROP TABLE IF EXISTS cache;
DROP TABLE IF EXISTS bookmarks;

CREATE TABLE cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_name TEXT NOT NULL,
    city TEXT NOT NULL,
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
    wiki_url TEXT,
    date TIMESTAMP NOT NULL
)
