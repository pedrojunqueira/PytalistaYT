from databricks.connect import DatabricksSession
import pytest

from pyspark.sql import Row

from src import functions

@pytest.fixture
def serverless():
  
  spark = DatabricksSession.builder.serverless(True).getOrCreate()
  return spark

def test_spark(serverless):
  df = serverless.createDataFrame(range(5))
  assert df.count() > 0

def test_transactions_from_datetime(serverless):
    ## assemble
    data = [
        {
            "creation_datetime": "2021-06-30 10:00:00",
            "value": "value1"
        },
        {
            "creation_datetime": "2021-07-01 00:00:00",
            "value": "value2"
        },
        {
            "creation_datetime": "2021-08-01 00:00:00",
            "value": "value3"
        }

    ]

    df = serverless.createDataFrame(map(lambda x: Row(**x), data))

    ## act
    result = functions.transactions_from_datetime(df, "2021-07-01")

    ## assert
    assert df.count() == 3
    assert result.count() == 2

  
  
