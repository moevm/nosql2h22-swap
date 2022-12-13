FROM python:3
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
 
WORKDIR /usr/src/swap
 
COPY ./requirements.txt /usr/src/swap/requirements.txt
 
RUN  pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/swap

RUN chmod +x entrypoint.sh 