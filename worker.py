import subprocess as sp
import time
import sys, os
import csv
import requests
# from scraper import *
from bs4 import BeautifulSoup
# from interruptingcow import timeout
from google.cloud import pubsub
# from google.cloud import monitoring


PROJECT = 'metrix-news'
TOPIC = 'scrape-queue-urls'
SUBSCRIPTION = 'scrape-sub-urls'
BUCKET = 'metrix-scraped-articles-data'

curr_url_count = 0
dead_urls = 0
unresponsive_urls = 0

def queue_empty(client):
    result = client.query(
        'pubsub.googleapis.com/subscription/num_undelivered_messages',
        minutes=1).as_dataframe()
    return result['pubsub_subscription'][PROJECT][SUBSCRIPTION][0] == 0

def print_message(message):
    print(message.data)
    message.ack()

def fetch_article_text(media_id, url):
    with open('article_corpus.csv','a') as fp:
        writer = csv.writer(fp)
        news_corpus_list = []
        article_text = ''
        try:
            # with timeout(4, exception = RuntimeError):
            try:
                print("checking media_id: {}".format(str(media_id)))
                url_result = requests.get(url)
            except:
                return
        except RuntimeError:
            print("...url took too long to respond, skipping")
            return
        if url_result.status_code == 404:
            # url is dead, continue with other urls
            print("...url gave a 404")
            return
        url_content = url_result.content
        soup = BeautifulSoup(url_content, features="html.parser")
        article_text = soup.find_all('p')
        corpus = ''
        for element in article_text:
            corpus += "\n" + ''.join(element.findAll(text = True))
        news_corpus_list.append(media_id)
        news_corpus_list.append(url)
        news_corpus_list.append(corpus)
        print(corpus)
        writer.writerow(news_corpus_list)
    # copy_to_gcs('article_corpus.csv')

def copy_to_gcs(csv_file):
    sp.check_call('gsutil mv {} gs://{}/tmp/scraped_data/'.format(csv_file, BUCKET), shell = True)

def handle_url(id_url):
    id_url_data = str(id_url.data)
    id = id_url_data.split('*****')[0]
    id = id.split('\'')[1]
    url = id_url_data.split('*****')[1]
    fetch_article_text(id, url)
    # copy_to_gcs(id)
    id_url.ack()

def main():
    # client = monitoring.Client(project=PROJECT)

    subscriber = pubsub.SubscriberClient()
    sub_path = 'projects/{}/subscriptions/{}'.format(PROJECT, SUBSCRIPTION)
    subscription = subscriber.subscribe(sub_path, callback = handle_url)

    time.sleep(60)

if __name__ == '__main__':
    main()
