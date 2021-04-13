FROM ubuntu:20.04

ENV listening_port 8000
ENV command "python manage.py runserver 0.0.0.0:${listening_port}"

EXPOSE ${listening_port}

RUN apt-get update
# RUN apt-get install software-properties-common -y && \
RUN apt-get install -y python-is-python3 python3-distutils curl python3-psycopg2 && \
    curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install Django==3.2 djangorestframework requests pillow

ADD ./ColoringWebapp /ColoringWebapp
WORKDIR /ColoringWebapp
RUN python manage.py makemigrations && python manage.py migrate

CMD ${command}