#!/bin/bash

# Set environment variables
export MYSQL_USER='RG_USER'
export MYSQL_PWD='RG_PASSWORD'
export MYSQL_HOST='localhost'
export MYSQL_DB='RG_DB'
export RG_API_HOST='0.0.0.0'
export RG_API_PORT='5000'
export RG_WEB_PORT='5050'

# Run API service on port 5000
echo "Starting API service on port $RG_API_PORT..."
gunicorn -w 4 -b $RG_API_HOST:$RG_API_PORT api.v1.app:app &

# Run Web Dynamic service on port 5050
echo "Starting Web Dynamic service on port $RG_WEB_PORT..."
gunicorn -w 4 -b $RG_API_HOST:$RG_WEB_PORT web_dynamic.app:app &
