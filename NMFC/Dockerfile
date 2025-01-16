FROM ubuntu

RUN apt-get -y update && \
# install python & dependencies
    apt install -y python3 && \
    apt install -y python3-selenium

# install google-chrome
RUN apt install -y wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    google-chrome --version && \
    rm -rf google-chrome-stable_current_amd64.deb && \
# install chromedriver
    apt install -y unzip && \
    wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm -rf chromedriver-linux64.zip

WORKDIR /app
COPY index.py .

ENTRYPOINT ["python3", "index.py"]