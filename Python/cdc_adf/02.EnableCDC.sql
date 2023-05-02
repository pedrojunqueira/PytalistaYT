EXEC sys.sp_cdc_enable_db 

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name = 'customers', 
@role_name = 'null',
@supports_net_changes = 1


select * from cdc.change_tables
select * from cdc.captured_columns
select * from cdc.ddl_history
select * from cdc.index_columns
select * from cdc.lsn_time_mapping
SELECT * from cdc.cdc_jobs

select name,
      is_tracked_by_cdc
 from sys.tables
 where is_tracked_by_cdc = 1


SELECT *
  FROM [cdc].[dbo_customers_CT]






