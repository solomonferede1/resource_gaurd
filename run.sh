#!/bin/bash

python3 -m venv venv
source venv/bin/activate

# Set environment variables
export MYSQL_USER='RG_USER'
export MYSQL_PWD='RG_PASSWORD'
export MYSQL_HOST='localhost'
export MYSQL_DB='RG_DB'
export RG_API_HOST='0.0.0.0'
export RG_API_PORT='5000'
export RG_WEB_PORT='5050'


# Install dependencies if not already installed
# pip3 install -r requirements.txt

# Start API service
echo "Starting API service on port $RG_API_PORT..."
gunicorn -w 4 -b $RG_API_HOST:$RG_API_PORT api.v1.app:app &

# Start Web Dynamic service
echo "Starting Web Dynamic service on port $RG_WEB_PORT..."
gunicorn -w 4 -b $RG_API_HOST:$RG_WEB_PORT web_dynamic.app:app &

# Keep the script running
wait