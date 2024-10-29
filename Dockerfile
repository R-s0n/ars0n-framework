FROM kalilinux/kali-rolling:latest

# Set environment variables (optional)
# ENV NODE_ENV=production

RUN apt-get update && apt-get install -y \
    curl \
    git \
    sudo \
    gnupg \
    wget \
    python3 \
    python3-pip \
    python3-flask-cors \
    awscli \
    nodejs \
    npm

RUN sh -c 'wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -; echo "deb [arch=amd64] https://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" >> /etc/apt/sources.list.d/mongodb-org-4.4.list'
RUN sudo apt-get update
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN sudo apt-get remove mongodb-server-core 
RUN sudo apt-get install -y mongodb-org
RUN mkdir -p /data/db
RUN rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash rs0n && \
    usermod -aG sudo rs0n && \
    echo "rs0n ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER rs0n

WORKDIR /usr/src/ars0n-framework

COPY . .

RUN sudo chmod 777 /usr/src/ars0n-framework/logs

RUN python3 install.py -d

EXPOSE 3000

ENTRYPOINT ["/entrypoint.sh"]
