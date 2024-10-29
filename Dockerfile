# Start from the official Debian base image
FROM kalilinux/kali-rolling:latest

# Set environment variables (optional)
# ENV NODE_ENV=production

# Install any dependencies you need here
# For example, if you need curl and git
 RUN apt-get update && apt-get install -y \
     curl \
     git \
     python3 \
     sudo \
     python3-pip \
     python3-flask-cors \
     awscli \
     nodejs \
     npm \
     && rm -rf /var/lib/apt/lists/*

# If your application is in Node, for example, install Node.js
# You may need to install build tools for other types of applications
RUN useradd -m -s /bin/bash rs0n && \
    usermod -aG sudo rs0n && \
    echo "rs0n ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER rs0n

# Create and set a working directory for your app
WORKDIR /usr/src/ars0n-framework

RUN sudo apt-get install gnupg curl
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
    sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
    --dearmor
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/8.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
RUN sudo apt-get update
RUN sudo apt-get install -y mongodb-org
RUN sudo systemctl start mongod

# Copy your application files into the container
COPY . .
RUN sudo chmod 777 /usr/src/ars0n-framework/logs

# Install application dependencies if necessary (for Node.js)
RUN ./install.sh

# Expose the port your application will run on
EXPOSE 3000

# Define the command to run your application
CMD ["npm", "start"]
