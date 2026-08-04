import logging
import datetime

today=datetime.datetime.now().date()
format_events ='%(asctime)s %(levelname)s: %(message)s'
format_data = '%(message)s'

#TODO: logs not switch on midnight if app will work for few days
logger_events = logging.getLogger("events")
logger_events.setLevel("INFO")
handler_for_events = logging.FileHandler(f"standard_log{today}.log",mode='a')
handler_for_events
handler_for_events.setFormatter(logging.Formatter(format_events))
logger_events.addHandler(handler_for_events)

logger_data = logging.getLogger("data")
logger_data.setLevel("INFO")
handler_for_data = logging.FileHandler(f"data_log{today}.log",mode='a')
handler_for_data.setFormatter(logging.Formatter(format_data))
logger_data.addHandler(handler_for_data)

