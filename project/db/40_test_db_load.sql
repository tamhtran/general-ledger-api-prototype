/* create test data from dev database
   except for transactions*/
DROP DATABASE IF EXISTS web_test;

CREATE DATABASE web_test
WITH TEMPLATE web_dev
OWNER postgres;

/* mock up test transactions
 */
 \c web_test;
TRUNCATE TABLE transactions;
INSERT INTO transactions (entry_no, date, country_id, account_id, details, amount)
VALUES
-- Transactions for account_id 10, region 1
('T1', '2021-01-01', 1, 10, 'Transaction 1', 100.00),
('T2', '2021-02-01', 1, 10, 'Transaction 2', -100.00),
('T3', '2021-03-01', 1, 10, 'Transaction 3', -5000.00), -- Negative amount

-- Transactions for account_id 20, region 3
('T4', '2021-04-01', 3, 20, 'Transaction 4', 150.00),
('T5', '2021-05-01', 3, 20, 'Transaction 5', 250.00),

-- More transactions for account_id 10, various regions
('T6', '2021-06-01', 1, 10, 'Transaction 6', 300.00),
('T7', '2021-06-30', 3, 10, 'Transaction 7', 400.00),

-- Transactions on the boundary of testing date range for account_id 20
('T8', '2021-07-01', 1, 20, 'Transaction 8', 500.00),
('T9', '2021-07-02', 2, 20, 'Transaction 9', 600.00);



