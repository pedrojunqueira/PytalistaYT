
-- table

SELECT [SalesOrderID]
      ,[SalesOrderDetailID]
      ,[OrderQty]
  FROM [AdventureWorks2019].[Sales].[SalesOrderDetail]

-- total full table

select sum(OrderQty) as Total
from Sales.SalesOrderDetail 

--select format(1000, '#,#')

-- Over without any parameter

select 
[SalesOrderID]
, OrderQty
,sum(OrderQty) over() as Total
from Sales.SalesOrderDetail 

-- partition
select 
[SalesOrderID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID ) as TotalForPartition 
from Sales.SalesOrderDetail 

-- Adding Order by
select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by [SalesOrderDetailID]) as Runningtotal 
from Sales.SalesOrderDetail 

-- it is a running total but why it is a running total
-- what if I wanted to control how I would like the agregation behave in the partition?
-- this is whay we need to understand the range/row clause

--https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16#order-by


select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by [SalesOrderDetailID]
		range between unbounded preceding AND current row) as runningtotal
from Sales.SalesOrderDetail 

-- the default value is  [range between unbounded preceding AND current row]

-- useless scenario

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID]
		range between unbounded preceding AND unbounded following) as totalWindow
from Sales.SalesOrderDetail 

-- reverse accumulation

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID] 
		range between current row AND unbounded following) as reverseTotal
from Sales.SalesOrderDetail 

-- more usefull one is rows
-- syntax is the same 
-- example of syntax

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID] 
		rows between unbounded preceding AND current row) as cumulative
from Sales.SalesOrderDetail

--but can add numbers of rows from the current

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum(OrderQty) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID] 
		rows between 2 preceding AND current row) as rollingSum
from Sales.SalesOrderDetail

-- moving average

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, sum (OrderQty) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID] 
		rows between 5 preceding AND current row) as rollingsum
, avg ( convert( decimal(18,4), OrderQty)) over( partition by SalesOrderID  order by SalesOrderID, [SalesOrderDetailID] 
		rows between 5 preceding AND current row) as rollingAvg
from Sales.SalesOrderDetail

-- other window function
-- row_number()

select * from(
select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, row_number() over(partition by [SalesOrderID] order by [SalesOrderID],  [SalesOrderDetailID] ) OrderOrder
from Sales.SalesOrderDetail ) a
where OrderOrder = 1

-- rank()
-- like PGA golf

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, rank() over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) Ranking
from Sales.SalesOrderDetail

-- dense_rank()
-- no jump

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, dense_rank() over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) Ranking
from Sales.SalesOrderDetail

-- lag

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, lag(OrderQty,1) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) PreviousItem
from Sales.SalesOrderDetail

-- lead

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, lag(OrderQty,1) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) PreviousItem
, lead(OrderQty,1) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) NextItem
from Sales.SalesOrderDetail

-- first value

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, first_value(OrderQty) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc) FirstItem
from Sales.SalesOrderDetail

-- last value

select
[SalesOrderID]
,[SalesOrderDetailID]
, OrderQty
, first_value(OrderQty) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc
  ) FirstItem
, last_value(OrderQty) over(partition by SalesOrderID order by [SalesOrderID], OrderQty desc
  rows between unbounded preceding AND unbounded following ) LastItem
from Sales.SalesOrderDetail


