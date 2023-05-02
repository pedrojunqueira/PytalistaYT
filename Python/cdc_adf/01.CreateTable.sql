create table customers 
(
customer_id int, 
first_name varchar(50), 
last_name varchar(50), 
email varchar(100), 
city varchar(50), CONSTRAINT "PK_Customers" PRIMARY KEY CLUSTERED ("customer_id") 
 );