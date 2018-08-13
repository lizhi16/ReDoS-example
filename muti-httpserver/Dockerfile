FROM django

RUN mkdir /handler

RUN mkdir /static

ADD ./handler/* /handler/

ADD ./static/* /static/

ADD  httpserver.py /

CMD ["python3","/httpserver.py","webapp","app"]

EXPOSE 8000
