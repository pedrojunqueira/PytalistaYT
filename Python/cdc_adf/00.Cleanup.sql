-- disable table

EXEC sys.sp_cdc_disable_table
    @source_schema = N'dbo',
    @source_name = N'customers',
    @capture_instance = N'dbo_customers'; 

-- clean up table

DECLARE @max_lsn binary(10) = sys.fn_cdc_get_max_lsn();
Exec sys.sp_cdc_cleanup_change_table
   @capture_instance = N'dbo_customers',
   @low_water_mark = @max_lsn;

-- disable cdc in the db

EXEC sys.sp_cdc_disable_db;

-- drop table

drop table customers 
