import sqlite3
import app.config.config as config

connection = sqlite3.connect(config.DB_ADDRESS)

with connection:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone_no TEXT NOT NULL,
            address TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('donor', 'admin'))
        );
    ''')

    connection.execute('''
           CREATE TABLE IF NOT EXISTS ngos (
               id TEXT PRIMARY KEY,
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL,
               phone_no TEXT NOT NULL,
               address TEXT NOT NULL,
               details TEXT NOT NULL
           );
       ''')
