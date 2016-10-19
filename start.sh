#!/usr/bin/env bash

port=$1
host=":9999"

docker-compose run -d -p $port$host pymosek
google-chrome "http://localhost:$port/tree"


