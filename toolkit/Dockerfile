FROM kalilinux/kali-rolling

WORKDIR /app
RUN mkdir /root/Tools
RUN mkdir /root/.keys
RUN touch /root/.keys/.hackerone
RUN touch /root/.keys/slack_web_hook
RUN touch /root/.keys/.keystore


ENV GOROOT=/usr/lib/go
ENV GOPATH=/root/go
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH

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
    massdns \
    curl \
    wget \
    vim \
    amass \
    jq \
    git \
    cewl \
    ffuf 

RUN apt update && \
    apt install -y --no-install-recommends \
    awscli \
    golang \
    chromium \
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

WORKDIR /app
COPY ./toolkit ./
RUN chmod -R 775 ./toolkit

EXPOSE 5000

CMD ["python3", "toolkit-service.py"]