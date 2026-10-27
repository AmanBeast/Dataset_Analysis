--  read group by properties

--  creating table
CREATE TABLE sales_data(

	sale_id SERIAL PRIMARY KEY,

	salesperson VARCHAR(50),

	region VARCHAR(30),

	product VARCHAR(30),

	sales_amount INT
);

--  Inserting values

INSERT INTO sales_data
(salesperson, region, product, sales_amount)
VALUES
('Rahul', 'North', 'Laptop', 50000),
('Neha', 'North', 'Mobile', 30000),
('Vivek', 'South', 'Laptop', 70000),
('Priya', 'East', 'Tablet', 45000),
('Amit', 'South', 'Mobile', 35000),
('Riya', 'East', 'Laptop', 80000),
('Karan', 'North', 'Tablet', 25000),
('Sohan', 'South', 'Laptop', 65000),
('Pooja', 'East', 'Mobile', 40000),
('Arjun', 'North', 'Laptop', 55000);

--  verify it
SELECT * FROM sales_data

--  before using CTE
--  let us solve a simple business question and find total sales by Region
SELECT region,SUM(sales_amount) as total_sales

from sales_data

group by region;

-- now, if the query becomes as follows
-- show the regions whose total sales exceed ₹160000
SELECT region,  SUM(sales_amount) as total_sales

from sales_data

group by region

having sum(sales_amount) > 160000;

-- where total_sales > 160000;

-- now, if the query becomes as follows
-- show the regions whose total sales exceed ₹160000

WITH region_sales AS (

SELECT region, SUM(sales_amount) As total_sales

FROM sales_data

GROUP BY region
)

SELECT * FROM region_sales

WHERE total_sales >16000;
)

-- here PostgreSQL will first execute this query, and
--  store this result temporarily as region_sales & tread it like a table, as stated

-- here the question is, it can be done without CTE, so why CTE
-- what if later we required: Total sales, average sales, region rank, top 2 regions
-- there the query becomes large

-- for every region show.
-- total sales, average sales, region rank, top 2 regions

-- as per our conventional approach
SELECT region, SUM(sales_amount) as total_sales, AVG(sales_amount) as avg_sales

FROM sales_data

GROUP BY region
ORDER by total_sales DESC
limit 2;

-- now we will use CTE to solve the same question
WITH region_summanry As (

SELECT region, SUM(sales_amount) AS total_sales, AVG(sales_amount) AS avg_sales

FROM sales_data

GROUP BY region

ORDER BY total_sales DESC

limit 2
)
SELECT * from region_summanry;

-- now region_summary behaves like a temporary table, and add rank 
WITH region_summary As (

SELECT region, SUM(sales_amount) AS total_sales, AVG(sales_amount) AS avg_sales

FROM sales_data

GROUP BY region

)
SELECT  region,total_sales,avg_sales,

DENSE_RANK() OVER (ORDER BY total_sales DESC) AS region_rank

FROM region_summary;

-- 
-- Total Sales by Product
SELECT product, SUM(sales_amount) as total_sales 

FROM sales_data

GROUP BY product
ORDER by total_sales DESC
limit 2;

-- Average sales 
SELECT product, AVG(sales_amount) as avg_sales 

FROM sales_data

GROUP BY product
ORDER by avg_sales DESC
limit 2;

-- Product rank
WITH product_summary As (

SELECT product, SUM(sales_amount) AS total_sales, AVG(sales_amount) AS avg_sales

FROM sales_data

GROUP BY product

)
SELECT  product,total_sales,avg_sales,

DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank

FROM product_summary;

-- Sales person rank
WITH sales_man As (

SELECT salesperson, SUM(sales_amount) AS total_sales, AVG(sales_amount) AS avg_sales

FROM sales_data

GROUP BY salesperson

)
SELECT  salesperson,total_sales,avg_sales,

DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_man

FROM sales_man
;
-- top 3 sales person
WITH sales_man As (

SELECT salesperson, SUM(sales_amount) AS total_sales, AVG(sales_amount) AS avg_sales

FROM sales_data

GROUP BY salesperson

)
SELECT  salesperson,total_sales,avg_sales,

DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_man

FROM sales_man
limit 3;