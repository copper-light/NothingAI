FROM python:3.10.14-alpine3.20
LABEL authors="handh"
COPY . /app
WORKDIR /app
RUN apk add gcc python3-dev musl-dev linux-headers && \
    pip install --upgrade pip &&  \
    pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
EXPOSE 80

