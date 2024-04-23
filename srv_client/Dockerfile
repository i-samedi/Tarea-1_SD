FROM python:3.8-slim

COPY ./srv_client /home/app
FROM grpcio/python:1.51.1

WORKDIR /home/app

RUN pip3.8 install --upgrade pip
RUN pip install --upgrade grpcio
RUN pip install --upgrade grpcio-tools
RUN pip3.8 install -r requirements.txt


CMD ["python3.8", "-u", "main.py"]
