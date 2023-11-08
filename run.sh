#!/bin/bash

sudo systemctl enable mongod 2>/dev/null
sudo systemctl start mongod 2>/dev/null
node server/server.js &
cd client
npm run start &
cd ../toolkit
python3 toolkit-service.py
