-- Reference: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
DROP TABLE IF EXISTS users;


DROP TABLE IF EXISTS files;


CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL,
        storage_gb NUMERIC NOT NULL DEFAULT 1.000
    );


CREATE UNIQUE INDEX username ON users (user_name);


CREATE TABLE
    files (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP,
        revision INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
