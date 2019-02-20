FROM arxiv/base:latest

WORKDIR /opt/arxiv/

RUN yum install -y python2-pip python2-devel mysql-devel sqlite

ADD Pipfile.lock /opt/arxiv/
RUN pip install -U pip pipenv
RUN pipenv install --ignore-pipfile

ADD abovl /opt/arxiv/abovl
ADD alembic /opt/arxiv/alembic
ADD alembic.ini bootstrap.py config.py uwsgi.ini uwsgi.py requirements.txt /opt/arxiv/

EXPOSE 8000
ENTRYPOINT ["pipenv", "run"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]
