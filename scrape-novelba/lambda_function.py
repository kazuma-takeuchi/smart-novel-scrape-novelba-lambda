import os
import re
import json
import time
import base64
import requests
import logging
from urllib.request import urlopen

from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime

from models import DEFAULT_DOCUMENT, NovelModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SITE_NAME = os.getenv('SITE_NAME')
BASE_URL = os.getenv('BASE_URL')


def get_html(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.content
    else:
        return None

        
def create_id(url):
    id_ = SITE_NAME + "-" + url.split('/')[-1]
    return id_


def jst_str2ts_epoch_milli(jst, format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.strptime(jst + "+0900", format + "%z")
    ts = dt.timestamp() * 1000
    return ts


def extract_attributes(html):
    soup = BeautifulSoup(html, "html.parser")
    document = {
        "title": soup.find("h1", class_="title").get_text(),
        "author": soup.find("p", class_="author").find("span").get_text(),
        "genre": soup.find("span", class_="ganre").get_text(),
        "tag": [t.get_text() for t in soup.find("ul", class_="keyword_list").findAll("a", class_="vivid_btn")],
        "description": re.sub(r"[\u3000\xa0\r]", "", soup.find("p", class_="detail").get_text()),
        "like_count": int(soup.find("ul", class_="repute_list").findAll("p", class_="count")[1].get_text()),
        "created_at": jst_str2ts_epoch_milli(soup.find("ul", class_="episode_list").find("time").get_text(), format="%Y/%m/%d"),
        "updated_time": jst_str2ts_epoch_milli(soup.find("p", class_="update").find("time").get_text(), format="%Y/%m/%d")
    }
    return document


def lambda_handler(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    logger.info(event)
    logger.info(f'event {event}')
    logger.info(f'BASE_URL = {BASE_URL}')
    url = BASE_URL + event['url']
    logger.info(f'scrape {url}')
    logger.info('BEGIN scraping')
    html = get_html(url)
    html = html.decode("utf-8")
    logger.info('END scraping')
    document = extract_attributes(html)
    id_ = create_id(url)
    document['key'] = id_
    document['url'] = url
    document['site_name'] = SITE_NAME
    document = NovelModel(**document).dict()
    res = {
        "document": document,
        "id": id_
    }
    return res