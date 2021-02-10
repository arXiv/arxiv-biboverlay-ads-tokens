FROM centos:centos8

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    APPLICATION_ROOT="/"
    
WORKDIR /opt/arxiv/

RUN yum install -y gcc python2-pip python2-devel mariadb-devel sqlite git

ADD Pipfile.lock /opt/arxiv/

RUN python2.7 -m pip install -U pip pipenv
RUN pipenv install --ignore-pipfile

ADD abovl /opt/arxiv/abovl
ADD alembic /opt/arxiv/alembic
ADD alembic.ini bootstrap.py config.py uwsgi.ini uwsgi.py requirements.txt /opt/arxiv/

EXPOSE 8000
ENTRYPOINT ["pipenv", "run"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]
