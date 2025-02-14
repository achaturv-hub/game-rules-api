FROM python:3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY main.py ./

RUN pip3 install -r /app/requirements.txt

CMD python ./main.py

EXPOSE 8000