FROM python:2.7
ADD . /assignment1
WORKDIR /assignment1
RUN pip install -r requirements.txt

EXPOSE 5000
