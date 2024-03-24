CREATE DATABASE web_dev;

\c web_dev;


CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS countries (
    country_id INTEGER PRIMARY KEY,
    name TEXT,
    region_id INTEGER REFERENCES regions(region_id)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    report TEXT,
    class_ TEXT,
    subclass TEXT,
    subclass2 TEXT,
    account TEXT,
    sub_account TEXT
);


CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY ,
    entry_no TEXT NOT NULL,
    date DATE NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(country_id),
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    details TEXT NOT NULL,
    amount DECIMAL
);

