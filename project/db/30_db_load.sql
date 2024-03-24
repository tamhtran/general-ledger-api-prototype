
\c web_dev;

/* load and transform account json file */
CREATE TABLE temp_accounts (data jsonb);
COPY temp_accounts (data) FROM '/tmp/data/accounts.jsonl';
insert into accounts(account_id, report, class_, subclass, subclass2, account, sub_account)
SELECT CAST(data->>'Account_key' AS INTEGER) AS account_id,
       data->>'Report' AS report,
       data->>'Class' AS class,
       data->>'SubClass' AS subclass,
       data->>'SubClass2' AS subclass2,
       data->>'Account' AS account,
       data->>'SubAccount' AS sub_account
FROM temp_accounts;
DROP TABLE  temp_accounts;


CREATE TABLE IF NOT EXISTS temp_transactions (
    entry_no TEXT,
    date TEXT,
    territory_key TEXT,
    account_key TEXT,
    details TEXT,
    amount TEXT
);

/*****************  load and transform transactions csv file  *****************/

COPY temp_transactions(entry_no, date, territory_key, account_key, details, amount)
    FROM '/tmp/data/gl_txn.csv' delimiter ',' csv header;

-- dedup if needed
 -- amount field is changed to be numeric
INSERT INTO transactions(entry_no, date, country_id, account_id, details, amount)
SELECT entry_no AS entry_no,
       CAST(date AS DATE) AS date,
       CAST(territory_key AS INTEGER) AS country_id,
       CAST(account_key AS INTEGER) AS account_id,
       details,
        CASE
        WHEN amount LIKE '%(%)%' THEN -1 * REPLACE(REPLACE(REPLACE(REPLACE(amount, '(', ''), ')', ''), ',', ''), '"', '')::NUMERIC
        ELSE REPLACE(REPLACE(REPLACE(amount, ',', ''), ' ', ''), '"', '')::NUMERIC
    END AS amount
FROM temp_transactions
group by entry_no, date, territory_key, account_key, details, amount;

DROP TABLE temp_transactions;


-- Create indexes
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_countries_region_id ON countries(region_id);

-- Optional: Composite index if queries often use both account_id and date together
CREATE INDEX idx_transactions_account_id_date ON transactions(account_id, date);

