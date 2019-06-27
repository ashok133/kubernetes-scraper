import time
import sys, os
import csv
import requests
from bs4 import BeautifulSoup
from interruptingcow import timeout
from google.cloud import pubsub
from google.cloud import monitoring
from tqdm import tqdm

url_dict = {}

PROJECT = 'metrix-news'
TOPIC = 'scrape-queue-urls'

def fetch_urls_from_csv(file_pointer):
    # global url_list
    csv_reader = csv.reader(file_pointer, delimiter = ',')
    next(csv_reader)
    for row in csv_reader:
        url_dict.update({row[0]:row[3]})
    return url_dict

def fetch_url_list(csv_file):
    with open(csv_file, 'r') as fp:
        url_dict = fetch_urls_from_csv(fp)
        url_list = list(url_dict.values())
        # url_list = url_list[1:]
    return url_dict

def main():
    csv_file_path = 'full_training.csv'
    url_dict = fetch_url_list(csv_file_path)
    publisher = pubsub.PublisherClient()
    topic_path = 'projects/{}/topics/{}'.format(PROJECT, TOPIC)
    for id, url in tqdm(url_dict.items()):
        id_url = str(id) + "*****" + url
        id_url = id_url.encode('utf-8')
        publisher.publish(topic_path, data = id_url)

if __name__ == '__main__':
    main()
