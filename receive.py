#!/usr/bin/env python
import pika
import traceback, sys
import json
import smtplib
import hashlib
'''
smtpObj = smtplib.SMTP('smtp.bk.ru', 587)
smtpObj.starttls()
smtpObj.login('backend.mipt@bk.ru','lolkek123')
smtpObj.sendmail("backend.mipt@bk.ru","geymer_98dsfdffhfjh764@mail.ru","hello)")
smtpObj.quit()
'''
conn_params = pika.URLParameters('amqp://localhost')
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue='reg-queue')
print("Waiting for messages. To exit press CTRL+C")

def valid(data: dict) -> bool:
    return len(data) == 2 and ('username' in data) and ('password' in data)

def callback(ch, method, properties, body):
    data = {}
    try:
        data = dict(eval(body))
    except Exception:
        print("user sent invalid request: invalid dict object")
        return
    if not valid(data):
        print("user sent invalid request: key set of dict object is not {'username', 'password'}")
        return
    data['password'] = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
    
    print(data)

channel.basic_consume(on_message_callback=callback, queue='reg-queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)
