create external location `ext-loc-cat`
url 'abfss://ext-uc@unitycatext.dfs.core.windows.net/catalogs/data'
with (storage credential `cred_ext`);

 create Catalog cat_sql
 managed location 'abfss://ext-uc@unitycatext.dfs.core.windows.net/catalogs/data';

 describe catalog extended cat_sql;

 create table cat_sql.default.names (id int, name string); 