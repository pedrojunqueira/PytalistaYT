

DECLARE  @from_lsn binary(10), @to_lsn binary(10);  
SET @from_lsn =sys.fn_cdc_get_min_lsn('dbo_customers');  
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than or equal',  GETDATE());
SELECT count(1) changecount FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, 'all')

DECLARE @begin_time datetime, @end_time datetime, @from_lsn binary(10), @to_lsn binary(10);
SET @begin_time = '2023-05-02 05:30:11.253';
SET @end_time = '2023-05-02 05:40:11.253' ;
SET @from_lsn = sys.fn_cdc_map_time_to_lsn('smallest greater than or equal', @begin_time);
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than', @end_time);
SELECT * FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, 'all')



DECLARE @from_lsn binary(10), @to_lsn binary(10); 
SET @from_lsn =sys.fn_cdc_get_min_lsn('dbo_customers'); 
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than or equal', GETDATE());
SELECT * FROM cdc.fn_cdc_get_net_changes_dbo_customers(@from_lsn, @to_lsn, 'all')


-- 2023-04-30 21:07:11.253
-- 2023-05-01 19:58:11.253
