FROM arxiv/base:latest

WORKDIR /opt/arxiv/
RUN yum install -y python2-pip python2-devel mysql-devel

ADD requirements*.txt /opt/arxiv/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-docker.txt

ADD . /opt/arxiv/

RUN rm /opt/arxiv/logs/* && \
    chmod 777 /opt/arxiv/logs /opt/arxiv/flask_session && \
    chown nobody:nobody /opt/arxiv/logs /opt/arxiv/flask_session

USER nobody
EXPOSE 8000
CMD cd /opt/arxiv && alembic upgrade head && uwsgi --ini uwsgi.ini
