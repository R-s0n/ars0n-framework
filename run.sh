#!/bin/bash

cleanup() {
    echo -e "\n\e[1mScript terminated. Cleaning up...\e[0m"
    pkill -P $$
    wait
    sudo fuser -k "5000/tcp"
    sleep 5
    echo -e "\e[1mCleanup completed.\e[0m"
    exit 0
}

user_prompt() {
    read -r -p "Processes are running on ports 8000, 3000, or 5000. Do you want to stop them? (y/n): " response
    case "$response" in
        [yY])
            for port in 8000 3000 5000; do
                if fuser "$port/tcp" > /dev/null 2>&1; then
                    echo "Stopping process running on port $port..."
                    sudo fuser -k "$port/tcp"
                    sleep 5 
                fi
            done
            ;;
        *)
            echo "Exiting the script without stopping processes."
            cleanup
            ;;
    esac
}

trap cleanup SIGTERM SIGINT

for port in 8000 3000 5000; do
    if fuser "$port/tcp" > /dev/null 2>&1; then
        user_prompt
        break  
    fi
done

if sudo docker exec mongodb-container mongosh --quiet --eval "db.runCommand({ connectionStatus: 1 })" > /dev/null 2>&1; then
    echo "MongoDB is running. Continuing..."
else
    echo "Error: MongoDB is not running! Please turn on your local MongoDB instance to use the Ars0n Framework. Exiting..."
    exit 1
fi

nohup node server/server.js > logs/server.log 2>&1 &
(
  cd client || { echo "Error: 'client' directory not found."; exit 1; }
  nohup npm run start > ../logs/client.log 2>&1 &
)
(
  cd toolkit || { echo "Error: 'toolkit' directory not found."; exit 1; }
  nohup python3 toolkit-service.py > ../logs/toolkit.log 2>&1 &
)

tail -f logs/toolkit.log &

wait
