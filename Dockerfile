# set base image (host OS)
FROM python:3.8

# Update the package manager and install necessary tools
RUN apt-get -y update && apt-get install -y curl nano wget nginx git

# Add the Yarn repository and key
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

# Add the MongoDB repository and key
RUN apt-get install -y gnupg curl
RUN curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update the package manager and install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Install Node.js v16
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN npm install yarn

# Set NODE_OPTIONS environment variable to enable legacy OpenSSL provider
ENV NODE_OPTIONS=--openssl-legacy-provider

# Install PIP
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

ENV ENV_TYPE staging
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
##########

ENV PYTHONPATH=$PYTHONPATH:/src/

# copy the dependencies file to the working directory
COPY src/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt