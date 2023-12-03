FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3-pip libcurl4-openssl-dev && pip3 install coverage unittest-xml-reporting requests
RUN useradd -ms /bin/bash runuser
USER runuser
WORKDIR /app
CMD ["bash"]
