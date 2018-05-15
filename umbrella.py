#!/usr/bin/env python
# umbrella.py
#
# Is it going to rain today (or tomorrow)?
#
# Requires an API key for Weather Underground:
# https://www.wunderground.com/weather/api/


import requests
from datetime import datetime, timedelta

APIKEY = "02eaaede6d650514"
LOCATION = "gb/sheffield"

URL_TEMPLATE = "http://api.wunderground.com/api/{APIKEY}/forecast/q/{LOCATION}.json"

def umbrella_today():
    # get the current date
    date = datetime.now()
    # if the current time is after 5pm, use tomorrow instead
    if date.hour >= 5:
        date += timedelta(1)
    date_tuple = (date.year, date.month, date.day)

    # download forecast from weather underground
    url = URL_TEMPLATE.format(APIKEY=APIKEY, LOCATION=LOCATION)
    r = requests.get(url)
    if not r.status_code == 200:
        raise RuntimeError("Request returned status code: {}".format(r.status_code))
    data = r.json()

    # order forecasts into dictionary {date: forecast}
    records = {}
    for record in data['forecast']['simpleforecast']['forecastday']:
        year = record['date']['year']
        month = record['date']['month']
        day = record['date']['day']
        records[(year, month, day)] = record

    # get forecast rainfall in millimetres
    forecast = records[date_tuple]
    rainfall_mm = forecast['qpf_day']['mm']

    if rainfall_mm is not None and rainfall_mm >= 1:
        return True
    else:
        return False

