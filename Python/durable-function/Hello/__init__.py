# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import pytz
from datetime import datetime
import time

def main(name: str) -> str:
    
    started = pytz.utc.localize(datetime.utcnow())
    
    logging.info(f"Processing {name} 😃")

    time.sleep(10)

    finished = pytz.utc.localize(datetime.utcnow())
    execution_time = (finished - started).seconds
    local = finished.astimezone(pytz.timezone("Australia/Adelaide"))

    logging.info(f"finished {name} 🚀 at {local.strftime('%Y%m%d %H:%M:%S %z')} executed in {execution_time} seconds")

    return f"Hello {name}! 🔥"
