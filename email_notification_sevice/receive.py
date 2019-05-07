#!/usr/bin/env python
import pika
import traceback, sys
import json
import smtplib
import hashlib
import datetime, time
import psycopg2
from itsdangerous import URLSafeTimedSerializer

while True:
    try:
        time.sleep(0)
        conn_params = pika.ConnectionParameters('rabbit', 5672)
        connection = pika.BlockingConnection(conn_params)
        channel = connection.channel()
        channel.queue_declare(queue='reg-queue')
        
        break
    except Exception:
        pass

print("Waiting for messages. To exit press CTRL+C")

def valid(data: dict) -> bool:
    return len(data) == 3 and ('username' in data) and ('email' in data) and ('datetime' in data)

def serialize_str(data) -> str:
    serializer = URLSafeTimedSerializer("code".encode('utf8'))
    
    user_id = serializer.dumps(
        data
    )
    
    return user_id

def make_email_body(serial: str) -> str:
    print("!")
    return 'Go here: http://127.0.0.1:5000/confirm/' + serial

def send_validation_code(username: str, email: str, datetime: str) -> bool:
    try:
        smtpObj = smtplib.SMTP('smtp.bk.ru', 587)
        smtpObj.starttls()
        smtpObj.login('backend.mipt@bk.ru','lolkek123')
        
        smtpObj.sendmail("backend.mipt@bk.ru", email, make_email_body(serialize_str([username, email, datetime])))
        smtpObj.quit()
        return True
    except Exception:
        return False

def callback(ch, method, properties, body):
    data = {}
    try:
        data = dict(eval(body))
    except Exception:
        print("user sent invalid request: invalid dict object")
        return
    if not valid(data):
        print(data)
        print("user sent invalid request: key set of dict object is not {'username', 'password'}")
        return
    
    if not send_validation_code(data['username'], data['email'], data['datetime']):
        print("registration of user {} failed on sending validation code".format(data['username']))
        return 

    print("registration code sended successfully to user {}".format(data['username']))    

channel.basic_consume(on_message_callback=callback, queue='reg-queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)

