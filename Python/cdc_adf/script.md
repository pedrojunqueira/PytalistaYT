## CDC = Change Data Capture

### What is CDC

Change data capture makes available in a convenient relational format the historical record 
of Data Manipulation Language (DML) activity that occurred on enabled tables. 

### Why CDC?

To make more efficient the ETL of larger tables and create a history.

## Doing this using ADF

### What  will you need

- Azure Subscription
    - Azure Data Factory
    - Azure Storage
    - Azure SQL DB

## Steps

I am following the [tutorial](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-change-data-capture-feature-portal) with some adaptations to Azure SQL DB and Parquet file format

1. Create a source table

```sql
create table customers 
(
customer_id int, 
first_name varchar(50), 
last_name varchar(50), 
email varchar(100), 
city varchar(50), CONSTRAINT "PK_Customers" PRIMARY KEY CLUSTERED ("customer_id") 
 );
```
2. Enable Data Capture

```sql
EXEC sys.sp_cdc_enable_db 

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name = 'customers', 
@role_name = 'null',
@supports_net_changes = 1
```

see in the database what objects where created in system tables

3. Populate some data

```sql
insert into customers 
     (customer_id, first_name, last_name, email, city) 
 values 
     (1, 'Chevy', 'Leward', 'cleward0@mapy.cz', 'Reading'),
     (2, 'Sayre', 'Ateggart', 'sateggart1@nih.gov', 'Portsmouth'),
    (3, 'Nathalia', 'Seckom', 'nseckom2@blogger.com', 'Portsmouth');
```

4. Create a Linked Service for the Azure SQL DB

- Enter Credentials
- Test Conncection

5. Create a Linked Service for the Azure Storage Account (Blob)

- Enter Credentials
- Test Conncection


6. Create a Source Dataset

`cdc.dbo_customer_CT`

7. Create a Destination Dataset (parquet)

`file_path` : "bronze"

8. Create a pipeline to copy the change data

9. Add a Lookup activity to check if any changes

add stored procedure (query)

```sql
DECLARE  @from_lsn binary(10), @to_lsn binary(10);  
SET @from_lsn =sys.fn_cdc_get_min_lsn('dbo_customers');  
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than or equal',  GETDATE());
SELECT count(1) changecount FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, 'all')
```

debug to check if it is running ok.

10. Add a if condition

connect to the previous activity

in the expression add this code to route to the true condition

`@greater(int(activity('GetChangeCount').output.firstRow.changecount),0)`

11. Add a placeholder wait activity to test if all is working so far

run `debug` 

12. Replace the wait activity by a copy activity

13. Configure the Source

use the SQL dataset

add this query for source

```sql
DECLARE @from_lsn binary(10), @to_lsn binary(10); 
SET @from_lsn =sys.fn_cdc_get_min_lsn('dbo_customers'); 
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than or equal', GETDATE());
SELECT * FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, 'all')
```

run `preview` and check if query is fine


14. Configure Sink 

USe the Parquet dataset

just for the first run dump file in the main container folder

publish all

15. Debug and check the storage if file is there

## Configure parameter to use tubling window trigger

16. Add parameter to the pipeline

`triggerStartTime` 
and 
`triggerEndTime`

in the default values use the format `YYYY-MM-DD HH24:MI:SS.FFF`

ensure the triggerStartTime is not prior to CDC being enabled on the table, otherwise this will result in an error.

run the stored procedure in sql to test if it is all good and that the dates where captured.

The dates is in UTC time.

17. change the query of the lookup activity to be parametrized

```sql
@concat('DECLARE @begin_time datetime, @end_time datetime, @from_lsn binary(10), @to_lsn binary(10); 
SET @begin_time = ''',pipeline().parameters.triggerStartTime,''';
SET @end_time = ''',pipeline().parameters.triggerEndTime,''';
SET @from_lsn = sys.fn_cdc_map_time_to_lsn(''smallest greater than or equal'', @begin_time);
SET @to_lsn = sys.fn_cdc_map_time_to_lsn(''largest less than'', @end_time);
SELECT count(1) changecount FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, ''all'')')
```
18. change the query of the copy activity to be also parametrized

```sql
@concat('DECLARE @begin_time datetime, @end_time datetime, @from_lsn binary(10), @to_lsn binary(10); 
SET @begin_time = ''',pipeline().parameters.triggerStartTime,''';
SET @end_time = ''',pipeline().parameters.triggerEndTime,''';
SET @from_lsn = sys.fn_cdc_map_time_to_lsn(''smallest greater than or equal'', @begin_time);
SET @to_lsn = sys.fn_cdc_map_time_to_lsn(''largest less than'', @end_time);
SELECT * FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, ''all'')')
```

19. Add parameter to the sink dataser

`triggerStart`


- add dynamic file path to save the parquet file in the directory part of the dataset

`@concat('customers/incremental/',formatDateTime(dataset().triggerStart,'yyyy/MM/dd'))`

- add dynamic file name to save parquet file with datetime tag

`@concat(formatDateTime(dataset().triggerStart,'yyyyMMddHHmmssfff'),'.parquet')`

20. Change configuration of the sink dataset in the copy activity

in the dataset parameter enter 

`@pipeline().parameters.triggerStartTime`

so the dataset gets the parameter of start time from the pipeline run

21. Click Debug to run all process

22. Check in the azure storage if the parquet file with the initial changes happened.

23. Run python scrip to check if parquet file is correct

make sure python enviroment is created activated and dependencies intalled

`python -m venv .venv`

`source .venv/bin/activate`

`python -m pip install --upgrade pip`

requirements.txt

```text
pandas
pyodbc
Faker
adlfs
```

`pip install -r requirements.txt`

`python read_parquet.py`

24. configure tumbling window trigger

click new trigger

chose tumbling window type

pick a start data like utc now

put recurrency every 5 minutes (minimum is 5)

no end

save

when start put a dynamic parameter to be passed to the pipeline.

for `triggerStartTime` 
`@formatDateTime(trigger().outputs.windowStartTime,'yyyy-MM-dd HH:mm:ss.fff')`

and 
for `triggerEndTime`
`@formatDateTime(trigger().outputs.windowEndTime,'yyyy-MM-dd HH:mm:ss.fff')`

25. Use the python script to add more transactions to the database

`python populate_table.py`

[ubuntu pyodbc driver](https://stackoverflow.com/questions/43417886/pyodbc-error-while-running-application-within-a-container)

[install SQL server driver ubuntu driver](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline)



26. Wait 5 minutes and check if trigger ran and parquet file was saved
