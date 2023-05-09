## Events Hub Kafka demo in Python

Event Hubs is a modern big data streaming platform and event ingestion service that can seamlessly integrate with other Azure and Microsoft services, such as Stream Analytics, Power BI, and Event Grid, along with outside services like Apache Spark. The service can process millions of events per second with low latency. The data sent to an event hub (Event Hubs instance) can be transformed and stored by using any real-time analytics providers or batching or storage adapters.


## Use Cases

- IoT
- Events Driven Architecture
- Real Time application
- Fraud Detection

## Demo

### create event hub in Azure and run producer and consumer in python

1. Sign in to Azure Portal
2. [Create](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-create) a Event Hub Resource
    a. tier needs to be Standard or above to use with Kafka
3. Create a topic
    a. chose 1 partition
    b. configure to capture data in azure storage
    c. create a consumer group [hubsconsumergroup]
4. Create a directory in your computer
    ```bash
    mkdir demo_kafka_events_hub
    cd demo_kafka_events_hub
    ```
5. Open VS code
    `code .`
6. create requirements file
    `touch requirements.txt`
add following packages in the file
```python
azure-eventhub
azure-eventhub-checkpointstoreblob-aio
```
7. create virtual environment and activate
```bash
python -m venv .venv
source .venv/bin/activate
```
8. upgrade pip and install requirements
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
9. create producer.py file

    update `EVENT_HUB_CONNECTION_STR` and `EVENT_HUB_NAME`
    variables to your name space

10. create consumer.py file

    update `EVENT_HUB_CONNECTION_STR` and `EVENT_HUB_NAME`
    also `BLOB_STORAGE_CONNECTION_STRING` and `BLOB_CONTAINER_NAME`
    variables to your name space

11. split the terminal window and run the consumer

    `python consumer.py`

12. in the other half of the terminal run the producer

    `python producer.py`

13. close terminal window

### run producer and consumer in python KAFKA Confluent

### in Azure portal

1. create a new topic

kafka_topic

2. create a new consumer group

kafka_consumer_group

3. create a subdir and change to it

    ```bash
    mkdir confluent
    cd confluent
    ```
4. create setup.sh file

```bash
#!/bin/bash
echo "Downloading/installing necessary dependencies"
sudo apt-get install git openssl libssl-dev build-essential python-pip python-dev librdkafka-dev
git clone https://github.com/edenhill/librdkafka

echo "Setting up librdkafka"
cd librdkafka
./configure
make
sudo make install
cd ..

echo "Setting up Confluent's Python Kafka library"
pip install confluent-kafka
echo "Try running the samples now!"
```

run `source setup.sh`

5. create a producer.py

update the conf `dict`

```python
 conf = {
        'bootstrap.servers': 'yournamespace.servicebus.windows.net:9093', #replace
        'security.protocol': 'SASL_SSL',
        'ssl.ca.location': '/usr/lib/ssl/certs/ca-certificates.crt', ## if you are using ubuntu
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': '<your-connection-string',          #replace
        'client.id': 'python-example-producer'
    }
```

6. create a consumer.py

update the conf `dict`

7. run the consumer

`python consumer.py kafka_consumer_group kafka_topic`

8. run the producer

`python producer.py kafka_topic`










