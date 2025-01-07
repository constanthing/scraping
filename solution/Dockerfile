FROM selenium/standalone-chrome:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

RUN pip3 install selenium

CMD ["python3", "index.py"]
