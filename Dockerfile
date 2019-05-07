FROM centos:7
RUN yum -y install bzip2 wget
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
bash ~/miniconda.sh -bfp /usr/local/miniconda
ENV PATH /usr/local/miniconda/bin:$PATH

RUN conda install python=3.6
RUN conda install -c anaconda postgresql 
RUN conda install psycopg2
RUN conda install -c anaconda flask
RUN conda config --add channels conda-forge
RUN conda install -c conda-forge flask-sqlalchemy 
RUN conda install -c conda-forge flask-migrate 
RUN conda install -c conda-forge flask-login
RUN conda install -c conda-forge flask-wtf

RUN wget https://www.rabbitmq.com/releases/erlang/erlang-18.2-1.el6.x86_64.rpm
RUN yum -y install erlang-18.2-1.el6.x86_64.rpm
RUN wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server-3.6.9-1.el7.noarch.rpm
RUN yum -y install rabbitmq-server-3.6.9-1.el7.noarch.rpm
RUN yum clean all



ADD . /code
WORKDIR /code

RUN conda install $(cat email_notification_sevice/requirements.txt)

#EXPOSE 80
EXPOSE 5000

ENTRYPOINT ["bash"]
ENV FLASK_APP=first_app.py
#CMD ["export FLASK_APP=first_app.py"]

ENTRYPOINT ["bash"]
ENV LC_ALL=en_IE.utf8
#CMD ["export LC_ALL=en_IE.utf8"]

CMD ["./run.sh"]
#CMD ["run"]

