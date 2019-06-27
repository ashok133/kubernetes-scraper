# sudo pip3 install google-cloud-pubsub

# sudo pip3 install google-cloud-monitoring

# sudo pip3 install -U googleapis-common-protos==1.5.10

# pubsub_example.py
from google.cloud import pubsub
from google.cloud import monitoring
import time

PROJECT = 'metrix-news'
TOPIC = 'scrape-queue'
SUBSCRIPTION = 'scraper-sub'


# This is a dirty hack since Pub/Sub doesn't expose a method for determining
# if the queue is empty (to my knowledge). We have to use the metrics API which
# is only updated every minute. Hopefully someone from Google can clarify!
def queue_empty(client):
    result = client.query(
        'pubsub.googleapis.com/subscription/num_undelivered_messages',
        minutes=1).as_dataframe()
    return result['pubsub_subscription'][PROJECT][SUBSCRIPTION][0] == 0


def print_message(message):
    print(message.data)
    message.ack()


def main():
    # client = monitoring.Client(project=PROJECT)

    # Publishes the message 'Hello World'
    publisher = pubsub.PublisherClient()
    topic_path = 'projects/{}/topics/{}'.format(PROJECT, TOPIC)
    data = 'Hello World'
    data = data.encode('utf-8')
    publisher.publish(topic_path, data = data)

    # Opens a connection to the message queue asynchronously
    subscriber = pubsub.SubscriberClient()
    sub_path = 'projects/{}/subscriptions/{}'.format(PROJECT, SUBSCRIPTION)
    subscription = subscriber.subscribe(sub_path, callback = print_message)
    # subscription.open(print_message)

    # Waits until the queue is empty to exit
    while (True):
        time.sleep(60)

if __name__ == '__main__':
    main()
