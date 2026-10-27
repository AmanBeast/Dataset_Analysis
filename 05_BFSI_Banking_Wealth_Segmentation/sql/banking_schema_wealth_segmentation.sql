-- create customer table
CREATE TABLE customers (
customer_id SERIAL PRIMARY KEY,
customer_name VARCHAR(50) NOT NULL,
email VARCHAR(100),
city VARCHAR(50)
);

-- create accounts table
CREATE TABLE accounts (
account_id SERIAL PRIMARY KEY,
customer_id INT,
account_type VARCHAR(20),
balance NUMERIC(10,2),
opening_date DATE,
FOREIGN KEY(customer_id)
REFERENCES customers(customer_id)
);

-- create transactions table
CREATE TABLE transactions (
transaction_id SERIAL PRIMARY KEY,
account_id INT,
transaction_date DATE,
transaction_type VARCHAR(20),
amount NUMERIC(10,2),
FOREIGN KEY(account_id)
REFERENCES accounts(account_id)
);

-- insert data into customers, provided that some values can be null
INSERT INTO customers
(customer_name, email, city)
VALUES
('Rahul Sharma','rahul@gmail.com','Delhi'),
('Neha Gupta',NULL,'Mumbai'),
('Vivek Kumar','vivek@gmail.com','Delhi'),
('Priya Singh',NULL,'Pune'),
('Amit Verma','amit@gmail.com','Chennai'),
('Riya Kapoor','riya@gmail.com','Mumbai'),
('Karan Malhotra',NULL,'Delhi'),
('Sohan Mehta','sohan@gmail.com','Pune');

-- insert data into accounts
INSERT INTO accounts
(customer_id, account_type, balance, opening_date)
VALUES
(1,'Savings',85000,'2022-01-15'),
(2,'Current',25000,'2023-03-20'),
(3,'Savings',120000,'2021-06-10'),
(4,'Savings',18000,'2024-01-05'),
(5,'Current',95000,'2020-08-25'),
(6,'Savings',150000,'2021-11-12'),
(7,'Current',12000,'2024-02-10'),
(8,'Savings',65000,'2022-09-18');

-- insert data into transactions
INSERT INTO transactions
(account_id, transaction_date, transaction_type, amount)
VALUES
(1,'2025-01-10','Deposit',10000),
(1,'2025-02-15','Withdrawal',5000),
(2,'2025-01-20','Deposit',8000),
(3,'2025-03-05','Deposit',15000),
(3,'2025-04-10','Withdrawal',7000),
(4,'2025-02-22','Deposit',4000),
(5,'2025-03-18','Deposit',12000),
(6,'2025-04-12','Withdrawal',10000),
(6,'2025-05-08','Deposit',20000),
(8,'2025-05-20','Deposit',9000);

-- question 1 - CASE WHEM
-- categorize customers as Premium,Regular or Low Balance based on their bank account

SELECT c.customer_name, a.balance,

CASE

WHEN a.balance >= 100000 THEN 'Premium Customer'

WHEN a.balance >= 50000 THEN 'Regular Customer'

ELSE 'Low Balance Customer'

END AS customer_category

FROM customers c

INNER JOIN accounts a

ON c.customer_id = a.customer_id;

-- question 2 COALESCE()
--  some customers have not provided email addresses
SELECT customer_name, COALESCE(email,'Email Not Available') As email
FROM customers;

-- check email, if email is NOT NULL, show email, if email is NULL then show 'Email Not Available'



--  it's significance
SELECT 1000 / NULLIF(0,0);

SELECT 1000 / NULLIF(5,0);

SELECT 1000 / (0);

SELECT 1000 / (5);

