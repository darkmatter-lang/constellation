#!/usr/bin/env bash

# Change directory to the current script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"; cd $DIR

docker build -t darkmatter-constellation:latest .
