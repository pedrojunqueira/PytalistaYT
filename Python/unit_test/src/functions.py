from pyspark.sql import functions as F

def transactions_from_datetime(df, from_datetime):
    return df.filter(F.col("creation_datetime") >= from_datetime)