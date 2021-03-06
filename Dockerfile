# Author: Dr. Konstantin Selyunin
# Date: 26 December 2019
# Version: v0.1
# License: MIT

# start from official ubuntu image
FROM ubuntu
# perform apt update
RUN apt-get update
# install wget for downloading files
# install curl for uploading build artifacts to the bitbucket cloud
RUN apt-get install wget curl -y
# installing pip3 gives python, c++, make, and others --> enough for our needs
RUN apt-get install python3.7 python3.7-dev -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt-get download python3-distutils
RUN dpkg-deb -x `realpath python3-distutils*.deb` /
RUN python3.7 get-pip.py
RUN pip install jinja2 pytest
WORKDIR /code
