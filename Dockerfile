FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./main.py main.py
COPY ./updating.py updating.py
COPY ./wrapper.sh wrapper.sh

CMD ["bash", "wrapper.sh"]