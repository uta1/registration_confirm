Чтобы начать работу напишите в терминале следующие команды:

sudo docker build -t pr .
docker run --network=host -it --rm -v $PWD:/pr pr bash

На этом моменте запустится новая shell.

export FLASK_APP=first_app.py
export LC_ALL=en_GB.utf8 
python3 email_notification_sevice/receive.py& 2> recieve_log
flask run
