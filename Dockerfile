FROM python:3.8-slim as compile-image

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/arxiv/

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install "poetry==1.1.4"

ADD pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
 poetry install --no-interaction --no-ansi

########### STAGE 2 ####################
FROM python:3.8-slim
ARG git_commit

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /opt/arxiv/
COPY --from=compile-image /opt/venv /opt/venv

RUN echo $git_commit > /git-commit.txt

ADD uwsgi.py uwsgi.ini ./

ADD abovl ./abovl

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]



