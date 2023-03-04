#!/bin/bash

sudo systemctl enable mongodb
sudo systemctl start mongodb
node server/server.js &
cd client
npm run start