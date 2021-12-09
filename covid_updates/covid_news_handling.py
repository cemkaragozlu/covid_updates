import requests
import sched
import time
import json
import logging

CONF = json.load(open("config.json", "r"))


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    api_key = CONF["news_api_key"]
    url = (
        'https://newsapi.org/v2/everything?'
        f'q={covid_terms}&'
        'from=2021-12-09&'
        'sortBy=popularity&'
        f'apiKey={api_key}')

    request = requests.get(url)
    logging.info(f"News API request status: {request}")
    return request.json()


def update_news(update_name):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(CONF.get("news_update_interval", 13), 2, news_API_request)
    s.run()
