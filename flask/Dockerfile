FROM python:3.7-alpine
 
RUN pip install gunicorn==19.9.0
 
COPY ./app.py /usr/src/app/
COPY ./conf.py /usr/src/app/
COPY ./requirements.txt /usr/src/app/
 
WORKDIR /usr/src/app/
RUN pip install -r requirements.txt
 
EXPOSE 5000