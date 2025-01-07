FROM ubuntu 

USER root

RUN apt-get -y update && apt upgrade

# install python & dependencies
RUN apt install -y python3
RUN apt install -y python3.12-venv
RUN apt install -y python3-selenium

# install google-chrome
RUN apt install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb
RUN google-chrome --version

# install chromedriver
RUN apt install -y unzip
RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip
RUN mv chromedriver-linux64/chromedriver /usr/local/bin/

WORKDIR /app
COPY . . 

CMD ["python3", "index.py"]
