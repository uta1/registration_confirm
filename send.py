#!/usr/bin/env python

import pika
import time
import json
import datetime

conn_params = [pika.URLParameters('amqp://localhost')]
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue='reg-queue')

username = "geymer_98"
dic = {
    "username": username,
    "email": username + "@mail.ru",
    "password": "pa",
    "datetime": str(datetime.datetime.utcnow())
}

channel.basic_publish(exchange='',
        routing_key='reg-queue',
        body=json.dumps(dic))
print(json.dumps(dic))

connection.close()
