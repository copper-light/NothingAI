FROM python:3.10.14-alpine3.20
LABEL authors="handh"
COPY ./apps /app/apps
COPY ./common /app/common
COPY ./config /app/config
COPY manage.py /app
COPY requirements.txt /app
COPY entrypoint.sh /

WORKDIR /app
RUN chmod +x /entrypoint.sh
RUN apk add gcc python3-dev musl-dev linux-headers && \
    pip install --upgrade pip &&  \
    pip install -r requirements.txt
#ENTRYPOINT /entrypoint.sh
CMD ["/entrypoint.sh"]
EXPOSE 80

