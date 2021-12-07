FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./

LABEL maintainer="rutger.smit@gmail.com"

ENV TWITTERHANDLE='rutgersmit'
ENV CHROMEDRIVER='http://192.168.100.10:4444/wd/hub'
ENV CHECKINTERVAL=120

CMD ["main.py"]
ENTRYPOINT ["python3"]

HEALTHCHECK CMD curl --fail https://twitter.com/ || exit 1
