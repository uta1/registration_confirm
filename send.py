#!/usr/bin/env python

import pika
import time
import json

from web_app.models import User
import pika
import time
import json

def sendEmail(User user)
	conn_params = [pika.URLParameters('amqp://localhost')]
	connection = pika.BlockingConnection(conn_params)
	channel = connection.channel()
	channel.queue_declare(queue='reg-queue')

	data = {'username': user.username, 'email': user.email, 'datetime': user.date_of_reg}
	channel.basic_publish(exchange='',
        routing_key='reg-queue',
        body=json.dumps(data))
	connection.close()

	print(json.dumps(dic))

	connection.close()
