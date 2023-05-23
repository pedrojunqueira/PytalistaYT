
import datetime
import logging

import azure.functions as func

route = func.Blueprint() 



@route.function_name(name="mytimer")
@route.schedule(schedule="*/5 * * * * *", arg_name="mytimer", run_on_startup=True,
              use_monitor=False) 
def test_function(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python 😃 timer trigger function ran at %s', utc_timestamp)