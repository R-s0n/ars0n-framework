FROM kalilinux/kali-rolling

WORKDIR /app
RUN mkdir ./Tools

ENV GOROOT=/usr/lib/go
ENV GOPATH=$HOME/go
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
    massdns \
    curl \
    wget \
    vim \
    amass \
    jq \
    git

RUN apt update && \
    apt install -y --no-install-recommends \
    awscli \
    golang \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/Tools
RUN git clone https://github.com/huntergregal/Sublist3r.git
RUN git clone https://github.com/hannob/tlshelpers.git
RUN git clone https://github.com/nsonaniya2010/SubDomainizer.git
RUN git clone https://github.com/rastating/dnmasscan.git
WORKDIR /app

RUN go install github.com/tomnomnom/assetfinder@latest
RUN go install github.com/lc/gau/v2/cmd/gau@latest
RUN go install github.com/incogbyte/shosubgo@latest
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN GO111MODULE=on go install github.com/jaeles-project/gospider@latest
RUN go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
RUN go install github.com/tomnomnom/httprobe@latest
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest


COPY ./toolkit ./

EXPOSE 5000

CMD ["python3", "toolkit-service.py"]