FROM kalilinux/kali-rolling

WORKDIR /app
RUN mkdir -p /root/Tools /root/.keys
RUN touch /root/.keys/.hackerone /root/.keys/slack_web_hook /root/.keys/.keystore

ENV GOROOT=/usr/lib/go
ENV GOPATH=/root/go
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH
ENV REDIS_URL: redis://redis:6379/0
ENV MONGO_URI: mongodb://root:example@mongodb:27017

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-flask \
    python3-flask-cors \
    python3-psutil \
    python3-requests \
    python3-dnspython \
    python3-termcolor \
    python3-bs4 \
    python3-htmlmin \
    python3-tldextract \
    python3-colorama \
    python3-cffi \
    python3-fastapi \
    python3-redis \
    python3-uvicorn \
    python3-celery \
    massdns \
    curl \
    wget \
    vim \
    amass \
    jq \
    git \
    cewl \
    ffuf \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y --no-install-recommends \
    awscli \
    golang \
    chromium \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/Tools
RUN git clone https://github.com/huntergregal/Sublist3r.git
RUN git clone https://github.com/hannob/tlshelpers.git
RUN git clone https://github.com/nsonaniya2010/SubDomainizer.git
RUN git clone https://github.com/rastating/dnmasscan.git
WORKDIR /root

RUN go install github.com/tomnomnom/assetfinder@latest
RUN go install github.com/lc/gau/v2/cmd/gau@latest
RUN go install github.com/incogbyte/shosubgo@latest
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN GO111MODULE=on go install github.com/jaeles-project/gospider@latest
RUN go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
RUN go install github.com/tomnomnom/httprobe@latest
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

WORKDIR /app
COPY ./toolkit ./  
RUN chmod -R 775 ./toolkit

EXPOSE 5000 6000 6379 