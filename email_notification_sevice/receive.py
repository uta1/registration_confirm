#!/usr/bin/env python
import pika
import traceback, sys
import json
import smtplib
import hashlib
import datetime, time
import psycopg2
from itsdangerous import URLSafeTimedSerializer

conn = psycopg2.connect(dbname='registration_confirm', user='postgres', 
                        password='passpsql', host='localhost')
cursor = conn.cursor()

conn_params = pika.URLParameters('amqp://localhost')
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue='reg-queue')

print("Waiting for messages. To exit press CTRL+C")

def valid(data: dict) -> bool:
    return len(data) == 4 and ('username' in data) and ('password' in data) and ('email' in data) and ('datetime' in data)

def serialize_str(data) -> str:
    serializer = URLSafeTimedSerializer("code".encode('utf8'))
    user_id = serializer.dumps(
        data
    )
    
    return user_id

'''
def prepare_registration(username: str, email: str, password_hash: str) -> bool:
    try:
        sql_query = 'insert into users values(%s,%s,%s,%s, NULL)'
        
        cursor.execute(sql_query, (username, password_hash, email, datetime.datetime.utcnow()))
        conn.commit()
        return True
    except Exception:
        try:
            conn.rollback()
            sql_query = 'select * from users where username=%s'
            cursor.execute(sql_query, (username,))
            conn.commit()
            
            confirmed = cursor.fetchall()[0][-1] is not None
            if confirmed:
                print("attempt to re-register")
                return False
                
            sql_query = 'update users set passhash=%s, registered=%s where username=%s'
            cursor.execute(sql_query, (password_hash, datetime.datetime.utcnow(), username,))
            conn.commit()
            
            return True
        except Exception:
            return False
'''

def send_validation_code(username: str, email: str, password_hash: str) -> bool:
    try:
        smtpObj = smtplib.SMTP('smtp.bk.ru', 587)
        smtpObj.starttls()
        smtpObj.login('backend.mipt@bk.ru','lolkek123')
        smtpObj.sendmail("backend.mipt@bk.ru", email, serialize_str([username, email, password_hash]) + " link  localhost:8080/confirm/" + serialize_str([username, email, password_hash]))
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
        print("user sent invalid request: key set of dict object is not {'username', 'password'}")
        return
        
    #password_hash = hash_str(data['password'])
    
    #if not prepare_registration(data['username'], data['email'], data['password']):
    #    print("registration of user {} failed on preparing".format(data['username']))
    #    return
    
    if not send_validation_code(data['username'], data['email'], data['password']):
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
